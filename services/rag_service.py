import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.config import Settings
from config import Config
import pandas as pd


class RAGService:
    def __init__(self):
        try:
            os.makedirs(Config.CHROMA_DIR, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path=Config.CHROMA_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name="startup_competitors",
                metadata={"description": "Startup competitor database"}
            )
            count = self.collection.count()
            print(f"✅ ChromaDB initialized with {count} documents")

            # Auto-populate if empty
            if count == 0:
                csv_path = os.path.join(Config.DATA_DIR, "synthetic_startups.csv")
                if os.path.exists(csv_path):
                    print("📊 Auto-populating ChromaDB from dataset...")
                    self.populate_from_dataset(csv_path)
                else:
                    print("⚠️ No dataset found — ChromaDB is empty")

        except Exception as e:
            print(f"⚠️ ChromaDB initialization error: {e}")
            self.collection = None

    def populate_from_dataset(self, dataset_path, max_entries=500):
        if self.collection is None:
            print("⚠️ ChromaDB not initialized")
            return
        try:
            existing_count = self.collection.count()
            if existing_count > 0:
                all_data = self.collection.get()
                if all_data['ids']:
                    self.collection.delete(ids=all_data['ids'])

            df = pd.read_csv(dataset_path, encoding="latin1")

            # Normalize column names
            col_map = {
                "primary_industry":       "primary_industry",
                "company_age_years":      "company_age_years",
                "employees_size_numeric": "employees_size_numeric",
                "total_funding_usd":      "total_funding_usd",
                "funding_rounds":         "funding_rounds",
                "investor_count":         "investor_count",
            }

            # Try to find industry column
            industry_col = next(
                (c for c in df.columns if "industry" in c.lower()), None
            )
            if industry_col is None:
                print("⚠️ No industry column found — using all rows")
                df["primary_industry"] = "Unknown"
            elif industry_col != "primary_industry":
                df = df.rename(columns={industry_col: "primary_industry"})

            df = df.dropna(subset=["primary_industry"])

            if "total_funding_usd" in df.columns:
                df = df[df["total_funding_usd"].notna() & (df["total_funding_usd"] > 0)]

            df = df.head(max_entries)

            documents, metadatas, ids = [], [], []

            for idx, row in df.iterrows():
                info = []
                if pd.notna(row.get("primary_industry")):
                    info.append(f"Industry: {row['primary_industry']}")
                if pd.notna(row.get("company_age_years")):
                    info.append(f"Age: {row['company_age_years']} years")
                if pd.notna(row.get("employees_size_numeric")):
                    info.append(f"Employees: {int(row['employees_size_numeric'])}")
                if pd.notna(row.get("total_funding_usd")):
                    info.append(f"Total Funding: ${row['total_funding_usd']/1_000_000:.2f}M")
                if pd.notna(row.get("funding_rounds")):
                    info.append(f"Rounds: {int(row['funding_rounds'])}")
                if pd.notna(row.get("investor_count")):
                    info.append(f"Investors: {int(row['investor_count'])}")

                if not info:
                    continue

                documents.append(" | ".join(info))
                metadatas.append({
                    "industry":  str(row.get("primary_industry", "Unknown")),
                    "age":       float(row.get("company_age_years") or 0),
                    "employees": int(row.get("employees_size_numeric") or 10),
                    "funding":   float(row.get("total_funding_usd") or 0),
                    "rounds":    int(row.get("funding_rounds") or 0),
                    "investors": int(row.get("investor_count") or 0),
                })
                ids.append(f"startup_{idx}")

            batch_size = 100
            for i in range(0, len(documents), batch_size):
                self.collection.add(
                    documents=documents[i:i+batch_size],
                    metadatas=metadatas[i:i+batch_size],
                    ids=ids[i:i+batch_size],
                )

            print(f"✅ Added {len(documents)} startups to ChromaDB")

        except Exception as e:
            print(f"❌ Error populating ChromaDB: {e}")
            import traceback
            traceback.print_exc()

    def query_competitors(self, query_text, n_results=5, industry_filter=None):
        if self.collection is None:
            return []
        try:
            count = self.collection.count()
            if count == 0:
                return []

            n_results = min(n_results, count)
            where_filter = {"industry": {"$eq": industry_filter}} if industry_filter else None

            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_filter
            )

            formatted = []
            if results and results["documents"]:
                for i in range(len(results["documents"][0])):
                    formatted.append({
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0,
                    })
            return formatted

        except Exception as e:
            print(f"❌ Error querying competitors: {e}")
            return []

    def get_competitor_summary(self, competitors):
        if not competitors:
            return "No competitors found in database."
        summary = ""
        for i, comp in enumerate(competitors, 1):
            summary += f"{i}. {comp.get('document', '')}\n\n"
        return summary.strip()


rag_service = RAGService()