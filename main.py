# # # """
# # # BizGenius FastAPI Backend
# # # Run:
# # #     cd server
# # #     uvicorn main:app --reload --port 8000
# # # """

# # # import os
# # # import json
# # # import warnings
# # # from datetime import datetime
# # # from io import BytesIO
# # # from typing import Any, Dict, List

# # # from dotenv import load_dotenv
# # # load_dotenv()

# # # import requests
# # # from fastapi import FastAPI, HTTPException, Query
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.responses import StreamingResponse
# # # from pydantic import BaseModel

# # # warnings.filterwarnings("ignore")

# # # # ───────────────── SERVICE IMPORTS ─────────────────
# # # ml_service: Any = None
# # # rag_service: Any = None
# # # llm_service: Any = None
# # # SERVICES_AVAILABLE = False

# # # try:
# # #     import sys
# # #     sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# # #     from services.ml_service  import ml_service
# # #     from services.rag_service import rag_service
# # #     from services.llm_service import llm_service

# # #     SERVICES_AVAILABLE = True
# # #     print("✅ Services loaded successfully")

# # # except Exception as e:
# # #     print("⚠ Running in STUB mode:", str(e))

# # # # ───────────────── APP SETUP ─────────────────
# # # app = FastAPI(title="BizGenius API", version="1.0.0")

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # ───────────────── MODELS ─────────────────

# # # class StartupInput(BaseModel):
# # #     domain: str
# # #     description: str
# # #     company_age: float
# # #     founder_count: int
# # #     employees: int
# # #     funding_rounds: int
# # #     funding_per_round: float
# # #     investor_count: int


# # # class CompetitorQuery(BaseModel):
# # #     query: str


# # # class AnalysisInput(BaseModel):
# # #     user_input: Dict
# # #     ml_results: Dict
# # #     competitors_text: str
# # #     probable_risks: List[str]


# # # class HierarchyInput(BaseModel):
# # #     user_input: Dict
# # #     ml_results: Dict
# # #     total_employees: int


# # # # ───────────────── ROUTES ─────────────────

# # # @app.get("/health")
# # # def health():
# # #     return {
# # #         "status": "ok",
# # #         "services_available": SERVICES_AVAILABLE,
# # #         "timestamp": datetime.now().isoformat(),
# # #     }


# # # # ─────────────── PREDICT ───────────────
# # # @app.post("/predict")
# # # def predict(body: StartupInput):

# # #     if SERVICES_AVAILABLE and ml_service:
# # #         try:
# # #             ml_results = ml_service.predict_startup_risk(
# # #                 company_age=body.company_age,
# # #                 founder_count=body.founder_count,
# # #                 employees=body.employees,
# # #                 funding_rounds=body.funding_rounds,
# # #                 funding_per_round=body.funding_per_round,
# # #                 investor_count=body.investor_count,
# # #             )
# # #             probable_risks = ml_service.get_probable_risks(body.dict(), ml_results)
# # #             ml_results["probable_risks"] = probable_risks
# # #             return ml_results

# # #         except Exception as e:
# # #             print("ML service error:", e)

# # #     # ── STUB ──
# # #     import random

# # #     sp = min(0.95, max(0.05, (
# # #         body.funding_rounds * 0.07
# # #         + body.founder_count * 0.08
# # #         + min(body.employees, 50) * 0.004
# # #         + body.investor_count * 0.03
# # #         + random.uniform(-0.1, 0.1)
# # #     )))

# # #     fp = max(0.02, 0.8 - sp)
# # #     up = max(0.02, 1 - sp - fp)

# # #     return {
# # #         "classification": "Success" if sp > 0.6 else "Failure",
# # #         "risk_level": "Low" if sp > 0.65 else "High",
# # #         "success_probability": round(sp, 4),
# # #         "probabilities": {
# # #             "success":   round(sp, 4),
# # #             "failure":   round(fp, 4),
# # #             "uncertain": round(up, 4),
# # #         },
# # #         "probable_risks": ["Market competition", "Funding runway"],
# # #     }


# # # # ─────────────── COMPETITORS ───────────────
# # # @app.post("/competitors")
# # # def competitors(body: CompetitorQuery):

# # #     if SERVICES_AVAILABLE and rag_service:
# # #         try:
# # #             comps = rag_service.query_competitors(body.query, n_results=5)
# # #             summary = rag_service.get_competitor_summary(comps)
# # #             return {"competitors": comps, "summary": summary}
# # #         except Exception as e:
# # #             print("RAG error:", e)

# # #     return {"competitors": [], "summary": "RAG not available"}


# # # # ─────────────── ANALYZE ───────────────
# # # @app.post("/analyze")
# # # def analyze(body: AnalysisInput):

# # #     if SERVICES_AVAILABLE and llm_service:
# # #         try:
# # #             analysis = llm_service.generate_analysis(
# # #                 body.user_input,
# # #                 body.ml_results,
# # #                 body.competitors_text,
# # #                 body.probable_risks,
# # #             )
# # #             return {"analysis": analysis}
# # #         except Exception as e:
# # #             print("LLM service error:", e)

# # #     return {"analysis": "LLM not configured. Add API key."}


# # # # ─────────────── HIERARCHY ───────────────
# # # @app.post("/hierarchy")
# # # def hierarchy(body: HierarchyInput):
# # #     return {
# # #         "ceo_title": "CEO",
# # #         "departments": [
# # #             {"name": "Engineering", "headcount": int(body.total_employees * 0.4)},
# # #             {"name": "Marketing",   "headcount": int(body.total_employees * 0.2)},
# # #             {"name": "Sales",       "headcount": int(body.total_employees * 0.2)},
# # #             {"name": "Operations",  "headcount": int(body.total_employees * 0.1)},
# # #             {"name": "HR",          "headcount": int(body.total_employees * 0.1)},
# # #         ],
# # #     }


# # # # ─────────────── NEWS ───────────────
# # # @app.get("/news")
# # # def news(domain: str = Query("SaaS")):
# # #     api_key = os.getenv("NEWS_API_KEY")

# # #     if not api_key:
# # #         return {"articles": [], "error": "Missing NEWS_API_KEY"}

# # #     try:
# # #         resp = requests.get(
# # #             "https://newsapi.org/v2/everything",
# # #             params={
# # #                 "q":        domain,
# # #                 "apiKey":   api_key,
# # #                 "pageSize": 15,
# # #                 "language": "en",
# # #                 "sortBy":   "publishedAt",
# # #             },
# # #         )
# # #         data = resp.json()
# # #         raw  = data.get("articles", [])

# # #         # ── Filter: must mention domain in title or description ──
# # #         domain_lower = domain.lower()
# # #         filtered = [
# # #             a for a in raw
# # #             if domain_lower in (a.get("title")       or "").lower()
# # #             or domain_lower in (a.get("description") or "").lower()
# # #         ]

# # #         # ── Fallback if strict filter returns nothing ──
# # #         articles = filtered[:8] if filtered else raw[:5]

# # #         # ── Normalize for frontend ──
# # #         normalized = [
# # #             {
# # #                 "title":       a.get("title", "No title"),
# # #                 "description": a.get("description", ""),
# # #                 "url":         a.get("url", "#"),
# # #                 "source":      a.get("source", {}).get("name", "Unknown"),
# # #                 "published":   a.get("publishedAt", ""),
# # #             }
# # #             for a in articles
# # #             if a.get("title") and "[Removed]" not in a.get("title", "")
# # #         ]

# # #         return {"articles": normalized}

# # #     except Exception as e:
# # #         return {"error": str(e), "articles": []}


# # # # ─────────────── ANALYTICS ───────────────
# # # @app.get("/analytics")
# # # def analytics():
# # #     try:
# # #         import pandas as pd
# # #         csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_startups.csv")
# # #         if os.path.exists(csv_path):
# # #             df = pd.read_csv(csv_path)
# # #             return {"data": df.to_dict(orient="records")}
# # #     except Exception as e:
# # #         print("Analytics error:", e)
# # #     return {"data": []}


# # # # ─────────────── PDF ───────────────
# # # @app.get("/download/pdf")
# # # def download_pdf():
# # #     from reportlab.pdfgen import canvas
# # #     from reportlab.lib.pagesizes import letter

# # #     buf = BytesIO()
# # #     c = canvas.Canvas(buf, pagesize=letter)
# # #     c.setFont("Helvetica-Bold", 20)
# # #     c.drawString(100, 750, "BizGenius Report")
# # #     c.setFont("Helvetica", 12)
# # #     c.drawString(100, 720, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
# # #     c.save()
# # #     buf.seek(0)

# # #     return StreamingResponse(buf, media_type="application/pdf",
# # #                              headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"})


# # # # ─────────────── MAIN ───────────────
# # # if __name__ == "__main__":
# # #     import uvicorn
# # #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# # """
# # BizGenius FastAPI Backend
# # Run:
# #     cd server
# #     uvicorn main:app --reload --port 8000
# # """

# # import os
# # import json
# # import warnings
# # from datetime import datetime
# # from io import BytesIO
# # from typing import Any, Dict, List

# # from dotenv import load_dotenv
# # load_dotenv()

# # import requests
# # from fastapi import FastAPI, HTTPException, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import StreamingResponse
# # from pydantic import BaseModel

# # warnings.filterwarnings("ignore")

# # # ───────────────── SERVICE IMPORTS ─────────────────
# # ml_service: Any = None
# # rag_service: Any = None
# # llm_service: Any = None
# # SERVICES_AVAILABLE = False

# # try:
# #     import sys
# #     sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# #     from services.ml_service  import ml_service
# #     from services.rag_service import rag_service
# #     from services.llm_service import llm_service
# #     SERVICES_AVAILABLE = True
# #     print("✅ Services loaded successfully")
# # except Exception as e:
# #     print("⚠ Running in STUB mode:", str(e))

# # app = FastAPI(title="BizGenius API", version="1.0.0")
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"], allow_credentials=True,
# #     allow_methods=["*"], allow_headers=["*"],
# # )

# # # ───────────────── MODELS ─────────────────
# # class StartupInput(BaseModel):
# #     domain: str
# #     description: str
# #     company_age: float
# #     founder_count: int
# #     employees: int
# #     funding_rounds: int
# #     funding_per_round: float
# #     investor_count: int

# # class CompetitorQuery(BaseModel):
# #     query: str

# # class AnalysisInput(BaseModel):
# #     user_input: Dict
# #     ml_results: Dict
# #     competitors_text: str
# #     probable_risks: List[str]

# # class HierarchyInput(BaseModel):
# #     user_input: Dict
# #     ml_results: Dict
# #     total_employees: int

# # class ReportInput(BaseModel):
# #     user_input: Dict
# #     ml_results: Dict
# #     analysis: str
# #     competitors: List[Dict]
# #     hierarchy: Dict
# #     probable_risks: List[str]

# # class PitchInput(BaseModel):
# #     user_input: Dict
# #     ml_results: Dict
# #     analysis: str
# #     competitors: List[Dict]
# #     hierarchy: Dict
# #     probable_risks: List[str]

# # # ───────────────── ROUTES ─────────────────
# # @app.get("/health")
# # def health():
# #     return {"status": "ok", "services_available": SERVICES_AVAILABLE,
# #             "timestamp": datetime.now().isoformat()}

# # @app.post("/predict")
# # def predict(body: StartupInput):
# #     if SERVICES_AVAILABLE and ml_service:
# #         try:
# #             ml_results = ml_service.predict_startup_risk(
# #                 company_age=body.company_age, founder_count=body.founder_count,
# #                 employees=body.employees, funding_rounds=body.funding_rounds,
# #                 funding_per_round=body.funding_per_round, investor_count=body.investor_count,
# #             )
# #             probable_risks = ml_service.get_probable_risks(body.dict(), ml_results)
# #             ml_results["probable_risks"] = probable_risks
# #             return ml_results
# #         except Exception as e:
# #             print("ML service error:", e)

# #     import random
# #     sp = min(0.95, max(0.05, (
# #         body.funding_rounds * 0.07 + body.founder_count * 0.08
# #         + min(body.employees, 50) * 0.004 + body.investor_count * 0.03
# #         + random.uniform(-0.1, 0.1)
# #     )))
# #     fp = max(0.02, 0.8 - sp)
# #     up = max(0.02, 1 - sp - fp)
# #     return {
# #         "classification": "Success" if sp > 0.6 else "Failure",
# #         "risk_level": "Low" if sp > 0.65 else "High",
# #         "success_probability": round(sp, 4),
# #         "probabilities": {"success": round(sp, 4), "failure": round(fp, 4), "uncertain": round(up, 4)},
# #         "probable_risks": ["Market competition", "Funding runway"],
# #     }

# # @app.post("/competitors")
# # def competitors(body: CompetitorQuery):
# #     if SERVICES_AVAILABLE and rag_service:
# #         try:
# #             comps = rag_service.query_competitors(body.query, n_results=5)
# #             summary = rag_service.get_competitor_summary(comps)
# #             return {"competitors": comps, "summary": summary}
# #         except Exception as e:
# #             print("RAG error:", e)
# #     return {"competitors": [], "summary": "RAG not available"}

# # @app.post("/analyze")
# # def analyze(body: AnalysisInput):
# #     if SERVICES_AVAILABLE and llm_service:
# #         try:
# #             analysis = llm_service.generate_analysis(
# #                 body.user_input, body.ml_results,
# #                 body.competitors_text, body.probable_risks,
# #             )
# #             return {"analysis": analysis}
# #         except Exception as e:
# #             print("LLM service error:", e)
# #     return {"analysis": "LLM not configured. Add API key."}

# # # ─────────────── HIERARCHY (LLM-powered) ───────────────
# # @app.post("/hierarchy")
# # def hierarchy(body: HierarchyInput):
# #     if SERVICES_AVAILABLE and llm_service:
# #         try:
# #             result = llm_service.generate_hierarchy(
# #                 body.user_input, body.ml_results, body.total_employees
# #             )
# #             return result
# #         except Exception as e:
# #             print("Hierarchy LLM error:", e)

# #     # Stub fallback
# #     emp = body.total_employees
# #     return {
# #         "ceo_title": "CEO & Co-Founder",
# #         "total_employees": emp,
# #         "departments": [
# #             {"name": "Engineering",  "headcount": int(emp * 0.4), "roles": ["CTO", "Backend Engineer", "Frontend Engineer"], "skills_needed": ["Python", "React", "AWS"]},
# #             {"name": "Marketing",    "headcount": int(emp * 0.2), "roles": ["CMO", "Growth Marketer"],                        "skills_needed": ["SEO", "Paid Ads", "Content"]},
# #             {"name": "Sales",        "headcount": int(emp * 0.2), "roles": ["VP Sales", "Account Executive"],                 "skills_needed": ["CRM", "Negotiation", "Outbound"]},
# #             {"name": "Operations",   "headcount": int(emp * 0.1), "roles": ["COO", "Operations Manager"],                    "skills_needed": ["Process Design", "Logistics"]},
# #             {"name": "HR",           "headcount": int(emp * 0.1), "roles": ["HR Manager", "Recruiter"],                      "skills_needed": ["Hiring", "Culture", "Compliance"]},
# #         ],
# #         "hiring_gaps": ["Senior Engineer", "Product Manager", "Data Analyst"],
# #         "recommended_next_hires": [
# #             {"role": "Product Manager", "priority": "High",   "reason": "Needed to define roadmap"},
# #             {"role": "Data Analyst",    "priority": "Medium", "reason": "Needed for growth metrics"},
# #         ]
# #     }

# # @app.get("/news")
# # def news(domain: str = Query("SaaS")):
# #     api_key = os.getenv("NEWS_API_KEY")
# #     if not api_key:
# #         return {"articles": [], "error": "Missing NEWS_API_KEY"}
# #     try:
# #         resp = requests.get("https://newsapi.org/v2/everything", params={
# #             "q": domain, "apiKey": api_key, "pageSize": 15,
# #             "language": "en", "sortBy": "publishedAt",
# #         })
# #         data = resp.json()
# #         raw  = data.get("articles", [])
# #         domain_lower = domain.lower()
# #         filtered = [a for a in raw
# #                     if domain_lower in (a.get("title") or "").lower()
# #                     or domain_lower in (a.get("description") or "").lower()]
# #         articles = filtered[:8] if filtered else raw[:5]
# #         normalized = [
# #             {"title": a.get("title","No title"), "description": a.get("description",""),
# #              "url": a.get("url","#"), "source": a.get("source",{}).get("name","Unknown"),
# #              "published": a.get("publishedAt","")}
# #             for a in articles if a.get("title") and "[Removed]" not in a.get("title","")
# #         ]
# #         return {"articles": normalized}
# #     except Exception as e:
# #         return {"error": str(e), "articles": []}

# # @app.get("/analytics")
# # def analytics():
# #     try:
# #         import pandas as pd
# #         csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_startups.csv")
# #         if os.path.exists(csv_path):
# #             df = pd.read_csv(csv_path)
# #             return {"data": df.to_dict(orient="records")}
# #     except Exception as e:
# #         print("Analytics error:", e)
# #     return {"data": []}

# # # ─────────────── PDF REPORT ───────────────
# # @app.post("/generate-report")
# # def generate_report(body: ReportInput):
# #     from services.report_service import generate_pdf_report
# #     buf = generate_pdf_report(body.dict())
# #     return StreamingResponse(buf, media_type="application/pdf",
# #                              headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"})

# # # ─────────────── PITCH DECK ───────────────
# # @app.post("/generate-pitch")
# # def generate_pitch(body: PitchInput):
# #     from services.pitch_service import generate_pitch_deck
# #     path = generate_pitch_deck(body.dict())
# #     with open(path, "rb") as f:
# #         content = f.read()
# #     os.remove(path)
# #     return StreamingResponse(
# #         BytesIO(content), media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
# #         headers={"Content-Disposition": "attachment; filename=bizgenius_pitch.pptx"}
# #     )

# # @app.get("/download/pdf")
# # def download_pdf():
# #     from reportlab.pdfgen import canvas
# #     from reportlab.lib.pagesizes import letter
# #     buf = BytesIO()
# #     c = canvas.Canvas(buf, pagesize=letter)
# #     c.setFont("Helvetica-Bold", 20)
# #     c.drawString(100, 750, "BizGenius Report")
# #     c.setFont("Helvetica", 12)
# #     c.drawString(100, 720, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
# #     c.save(); buf.seek(0)
# #     return StreamingResponse(buf, media_type="application/pdf",
# #                              headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"})

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# """
# BizGenius FastAPI Backend
# Run:
#     cd server
#     uvicorn main:app --reload --port 8000
# """

# import os
# import json
# import warnings
# from datetime import datetime
# from io import BytesIO
# from typing import Any, Dict, List

# from dotenv import load_dotenv
# load_dotenv()

# import requests
# from fastapi import FastAPI, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel

# warnings.filterwarnings("ignore")

# # ───────────────── SERVICE IMPORTS ─────────────────
# ml_service: Any = None
# rag_service: Any = None
# llm_service: Any = None
# SERVICES_AVAILABLE = False

# try:
#     import sys
#     sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
#     from services.ml_service  import ml_service
#     from services.rag_service import rag_service
#     from services.llm_service import llm_service
#     SERVICES_AVAILABLE = True
#     print("✅ Services loaded successfully")
# except Exception as e:
#     print("⚠ Running in STUB mode:", str(e))

# app = FastAPI(title="BizGenius API", version="1.0.0")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# # ───────────────── MODELS ─────────────────
# class StartupInput(BaseModel):
#     domain: str
#     description: str
#     company_age: float
#     founder_count: int
#     employees: int
#     funding_rounds: int
#     funding_per_round: float
#     investor_count: int

# class CompetitorQuery(BaseModel):
#     query: str

# class AnalysisInput(BaseModel):
#     user_input: Dict
#     ml_results: Dict
#     competitors_text: str
#     probable_risks: List[str]

# class HierarchyInput(BaseModel):
#     user_input: Dict
#     ml_results: Dict
#     total_employees: int

# # ── NEW: Hiring Guide input model ──────────────────
# class HiringGuideInput(BaseModel):
#     user_input: Dict
#     ml_results: Dict
#     hierarchy: Dict

# class ReportInput(BaseModel):
#     user_input: Dict
#     ml_results: Dict
#     analysis: str
#     competitors: List[Dict]
#     hierarchy: Dict
#     probable_risks: List[str]
#     hiring_guide: Dict = {} 

# class PitchInput(BaseModel):
#     user_input: Dict
#     ml_results: Dict
#     analysis: str
#     competitors: List[Dict]
#     hierarchy: Dict
#     probable_risks: List[str]
#     hiring_guide: Dict = {} 

# # ───────────────── ROUTES ─────────────────
# @app.get("/health")
# def health():
#     return {"status": "ok", "services_available": SERVICES_AVAILABLE,
#             "timestamp": datetime.now().isoformat()}

# @app.post("/predict")
# def predict(body: StartupInput):
#     if SERVICES_AVAILABLE and ml_service:
#         try:
#             ml_results = ml_service.predict_startup_risk(
#                 company_age=body.company_age, founder_count=body.founder_count,
#                 employees=body.employees, funding_rounds=body.funding_rounds,
#                 funding_per_round=body.funding_per_round, investor_count=body.investor_count,
#             )
#             probable_risks = ml_service.get_probable_risks(body.dict(), ml_results)
#             ml_results["probable_risks"] = probable_risks
#             return ml_results
#         except Exception as e:
#             print("ML service error:", e)

#     import random
#     sp = min(0.95, max(0.05, (
#         body.funding_rounds * 0.07 + body.founder_count * 0.08
#         + min(body.employees, 50) * 0.004 + body.investor_count * 0.03
#         + random.uniform(-0.1, 0.1)
#     )))
#     fp = max(0.02, 0.8 - sp)
#     up = max(0.02, 1 - sp - fp)
#     return {
#         "classification": "Success" if sp > 0.6 else "Failure",
#         "risk_level": "Low" if sp > 0.65 else "High",
#         "success_probability": round(sp, 4),
#         "probabilities": {"success": round(sp, 4), "failure": round(fp, 4), "uncertain": round(up, 4)},
#         "probable_risks": ["Market competition", "Funding runway"],
#     }

# @app.post("/competitors")
# def competitors(body: CompetitorQuery):
#     if SERVICES_AVAILABLE and rag_service:
#         try:
#             comps = rag_service.query_competitors(body.query, n_results=5)
#             summary = rag_service.get_competitor_summary(comps)
#             return {"competitors": comps, "summary": summary}
#         except Exception as e:
#             print("RAG error:", e)
#     return {"competitors": [], "summary": "RAG not available"}

# @app.post("/analyze")
# def analyze(body: AnalysisInput):
#     if SERVICES_AVAILABLE and llm_service:
#         try:
#             analysis = llm_service.generate_analysis(
#                 body.user_input, body.ml_results,
#                 body.competitors_text, body.probable_risks,
#             )
#             return {"analysis": analysis}
#         except Exception as e:
#             print("LLM service error:", e)
#     return {"analysis": "LLM not configured. Add API key."}

# # ─────────────── HIERARCHY (LLM-powered) ───────────────
# @app.post("/hierarchy")
# def hierarchy(body: HierarchyInput):
#     if SERVICES_AVAILABLE and llm_service:
#         try:
#             result = llm_service.generate_hierarchy(
#                 body.user_input, body.ml_results, body.total_employees
#             )
#             return result
#         except Exception as e:
#             print("Hierarchy LLM error:", e)

#     emp = body.total_employees
#     return {
#         "ceo_title": "CEO & Co-Founder",
#         "total_employees": emp,
#         "departments": [
#             {"name": "Engineering",  "headcount": int(emp * 0.4), "roles": ["CTO", "Backend Engineer", "Frontend Engineer"], "skills_needed": ["Python", "React", "AWS"]},
#             {"name": "Marketing",    "headcount": int(emp * 0.2), "roles": ["CMO", "Growth Marketer"],                        "skills_needed": ["SEO", "Paid Ads", "Content"]},
#             {"name": "Sales",        "headcount": int(emp * 0.2), "roles": ["VP Sales", "Account Executive"],                 "skills_needed": ["CRM", "Negotiation", "Outbound"]},
#             {"name": "Operations",   "headcount": int(emp * 0.1), "roles": ["COO", "Operations Manager"],                    "skills_needed": ["Process Design", "Logistics"]},
#             {"name": "HR",           "headcount": int(emp * 0.1), "roles": ["HR Manager", "Recruiter"],                      "skills_needed": ["Hiring", "Culture", "Compliance"]},
#         ],
#         "hiring_gaps": ["Senior Engineer", "Product Manager", "Data Analyst"],
#         "recommended_next_hires": [
#             {"role": "Product Manager", "priority": "High",   "reason": "Needed to define roadmap"},
#             {"role": "Data Analyst",    "priority": "Medium", "reason": "Needed for growth metrics"},
#         ]
#     }

# # ─────────────── HIRING GUIDE (LLM-powered) ────────────
# @app.post("/hiring-guide")
# def hiring_guide(body: HiringGuideInput):
#     if SERVICES_AVAILABLE and llm_service:
#         try:
#             result = llm_service.generate_hiring_guide(
#                 body.user_input, body.ml_results, body.hierarchy
#             )
#             return result
#         except Exception as e:
#             print("Hiring guide LLM error:", e)

#     # Stub fallback
#     # In the stub /predict return block, replace the return with:
#     return {
#     "classification": "Success" if sp > 0.6 else "Failure",
#     "risk_level": "Low" if sp > 0.65 else "High",
#     "success_probability": round(sp, 4),
#     "predicted_funding_usd": round(body.funding_per_round * (body.funding_rounds + 1), 2),  # ← ADD THIS
#     "probabilities": {"success": round(sp, 4), "failure": round(fp, 4), "uncertain": round(up, 4)},
#     "probable_risks": ["Market competition", "Funding runway"],
#    }

# @app.get("/news")
# def news(domain: str = Query("SaaS")):
#     api_key = os.getenv("NEWS_API_KEY")
#     if not api_key:
#         return {"articles": [], "error": "Missing NEWS_API_KEY"}
#     try:
#         resp = requests.get("https://newsapi.org/v2/everything", params={
#             "q": domain, "apiKey": api_key, "pageSize": 15,
#             "language": "en", "sortBy": "publishedAt",
#         })
#         data = resp.json()
#         raw  = data.get("articles", [])
#         domain_lower = domain.lower()
#         filtered = [a for a in raw
#                     if domain_lower in (a.get("title") or "").lower()
#                     or domain_lower in (a.get("description") or "").lower()]
#         articles = filtered[:8] if filtered else raw[:5]
#         normalized = [
#             {"title": a.get("title","No title"), "description": a.get("description",""),
#              "url": a.get("url","#"), "source": a.get("source",{}).get("name","Unknown"),
#              "published": a.get("publishedAt","")}
#             for a in articles if a.get("title") and "[Removed]" not in a.get("title","")
#         ]
#         return {"articles": normalized}
#     except Exception as e:
#         return {"error": str(e), "articles": []}

# @app.get("/analytics")
# def analytics():
#     try:
#         import pandas as pd
#         csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_startups.csv")
#         if os.path.exists(csv_path):
#             df = pd.read_csv(csv_path)
#             return {"data": df.to_dict(orient="records")}
#     except Exception as e:
#         print("Analytics error:", e)
#     return {"data": []}

# # ─────────────── PDF REPORT ───────────────
# @app.post("/generate-report")
# def generate_report(body: ReportInput):
#     from services.report_service import generate_pdf_report
#     buf = generate_pdf_report(body.dict())
#     return StreamingResponse(buf, media_type="application/pdf",
#                              headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"})

# # ─────────────── PITCH DECK ───────────────
# @app.post("/generate-pitch")
# def generate_pitch(body: PitchInput):
#     from services.pitch_service import generate_pitch_deck
#     path = generate_pitch_deck(body.dict())
#     with open(path, "rb") as f:
#         content = f.read()
#     os.remove(path)
#     return StreamingResponse(
#         BytesIO(content), media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
#         headers={"Content-Disposition": "attachment; filename=bizgenius_pitch.pptx"}
#     )

# @app.get("/download/pdf")
# def download_pdf():
#     from reportlab.pdfgen import canvas
#     from reportlab.lib.pagesizes import letter
#     buf = BytesIO()
#     c = canvas.Canvas(buf, pagesize=letter)
#     c.setFont("Helvetica-Bold", 20)
#     c.drawString(100, 750, "BizGenius Report")
#     c.setFont("Helvetica", 12)
#     c.drawString(100, 720, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
#     c.save(); buf.seek(0)
#     return StreamingResponse(buf, media_type="application/pdf",
#                              headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
BizGenius FastAPI Backend
Run:
    cd server
    uvicorn main:app --reload --port 8000
"""

import os
import json
import warnings
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List

from dotenv import load_dotenv
load_dotenv()

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

warnings.filterwarnings("ignore")

# ───────────────── SERVICE IMPORTS ─────────────────
ml_service:  Any = None
rag_service: Any = None
llm_service: Any = None
SERVICES_AVAILABLE = False

try:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from services.ml_service  import ml_service
    from services.rag_service import rag_service
    from services.llm_service import llm_service
    SERVICES_AVAILABLE = True
    print("✅ Services loaded successfully")
except Exception as e:
    print("⚠ Running in STUB mode:", str(e))

app = FastAPI(title="BizGenius API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


# ───────────────── PYDANTIC MODELS ─────────────────
class StartupInput(BaseModel):
    domain: str
    description: str
    company_age: float
    founder_count: int
    employees: int
    funding_rounds: int
    funding_per_round: float
    investor_count: int

class CompetitorQuery(BaseModel):
    query: str

class AnalysisInput(BaseModel):
    user_input: Dict
    ml_results: Dict
    competitors_text: str
    probable_risks: List[str]

class HierarchyInput(BaseModel):
    user_input: Dict
    ml_results: Dict
    total_employees: int

class HiringGuideInput(BaseModel):
    user_input: Dict
    ml_results: Dict
    hierarchy: Dict

class ReportInput(BaseModel):
    user_input: Dict
    ml_results: Dict
    analysis: str
    competitors: List[Dict]
    hierarchy: Dict
    probable_risks: List[str]
    hiring_guide: Dict = {}

class PitchInput(BaseModel):
    user_input: Dict
    ml_results: Dict
    analysis: str
    competitors: List[Dict]
    hierarchy: Dict
    probable_risks: List[str]
    hiring_guide: Dict = {}


# ───────────────── ROUTES ──────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "services_available": SERVICES_AVAILABLE,
        "timestamp": datetime.now().isoformat(),
    }


# ─── ML Prediction ────────────────────────────────
@app.post("/predict")
def predict(body: StartupInput):
    if SERVICES_AVAILABLE and ml_service:
        try:
            ml_results = ml_service.predict_startup_risk(
                company_age=body.company_age,
                founder_count=body.founder_count,
                employees=body.employees,
                funding_rounds=body.funding_rounds,
                funding_per_round=body.funding_per_round,
                investor_count=body.investor_count,
            )
            probable_risks = ml_service.get_probable_risks(body.dict(), ml_results)
            ml_results["probable_risks"] = probable_risks
            return ml_results
        except Exception as e:
            print("ML service error:", e)

    # ── Stub fallback (no ML available) ──
    import random
    sp = min(0.95, max(0.05, (
        body.funding_rounds * 0.07
        + body.founder_count * 0.08
        + min(body.employees, 50) * 0.004
        + body.investor_count * 0.03
        + random.uniform(-0.1, 0.1)
    )))
    fp = max(0.02, 0.8 - sp)
    up = max(0.02, 1.0 - sp - fp)

    # predicted_funding_usd is required by the PDF report — never omit it
    predicted_funding = round(body.funding_per_round * (body.funding_rounds + 1), 2)

    return {
        "classification":        "Success" if sp > 0.6 else "Failure",
        "risk_level":            "Low"     if sp > 0.65 else "High",
        "success_probability":   round(sp, 4),
        "predicted_funding_usd": predicted_funding,
        "probabilities": {
            "success":   round(sp, 4),
            "failure":   round(fp, 4),
            "uncertain": round(up, 4),
        },
        "probable_risks": ["Market competition", "Funding runway"],
    }


# ─── Competitors (RAG) ────────────────────────────
@app.post("/competitors")
def competitors(body: CompetitorQuery):
    if SERVICES_AVAILABLE and rag_service:
        try:
            comps   = rag_service.query_competitors(body.query, n_results=5)
            summary = rag_service.get_competitor_summary(comps)
            return {"competitors": comps, "summary": summary}
        except Exception as e:
            print("RAG error:", e)
    return {"competitors": [], "summary": "RAG not available"}


# ─── LLM Strategic Analysis ───────────────────────
@app.post("/analyze")
def analyze(body: AnalysisInput):
    if SERVICES_AVAILABLE and llm_service:
        try:
            analysis = llm_service.generate_analysis(
                body.user_input, body.ml_results,
                body.competitors_text, body.probable_risks,
            )
            return {"analysis": analysis}
        except Exception as e:
            print("LLM service error:", e)
    return {"analysis": "LLM not configured. Add GROQ_API_KEY to .env"}


# ─── Team Hierarchy (Groq LLM) ────────────────────
@app.post("/hierarchy")
def hierarchy(body: HierarchyInput):
    if SERVICES_AVAILABLE and llm_service:
        try:
            result = llm_service.generate_hierarchy(
                body.user_input, body.ml_results, body.total_employees
            )
            return result
        except Exception as e:
            print("Hierarchy LLM error:", e)

    # ── Stub fallback ──
    emp = body.total_employees
    return {
        "ceo_title":       "CEO & Co-Founder",
        "total_employees": emp,
        "departments": [
            {
                "name": "Engineering",
                "headcount": int(emp * 0.4),
                "roles": ["CTO", "Backend Engineer", "Frontend Engineer"],
                "skills_needed": ["Python", "React", "AWS"],
            },
            {
                "name": "Marketing",
                "headcount": int(emp * 0.2),
                "roles": ["CMO", "Growth Marketer"],
                "skills_needed": ["SEO", "Paid Ads", "Content"],
            },
            {
                "name": "Sales",
                "headcount": int(emp * 0.2),
                "roles": ["VP Sales", "Account Executive"],
                "skills_needed": ["CRM", "Negotiation", "Outbound"],
            },
            {
                "name": "Operations",
                "headcount": int(emp * 0.1),
                "roles": ["COO", "Operations Manager"],
                "skills_needed": ["Process Design", "Logistics"],
            },
            {
                "name": "HR",
                "headcount": int(emp * 0.1),
                "roles": ["HR Manager", "Recruiter"],
                "skills_needed": ["Hiring", "Culture", "Compliance"],
            },
        ],
        "hiring_gaps": ["Senior Engineer", "Product Manager", "Data Analyst"],
        "recommended_next_hires": [
            {"role": "Product Manager", "priority": "High",   "reason": "Needed to define roadmap"},
            {"role": "Data Analyst",    "priority": "Medium", "reason": "Needed for growth metrics"},
        ],
        "org_insight": (
            "This structure is optimized for an early-stage startup: "
            "engineering-heavy to move fast, lean marketing and sales to validate "
            "the market, and a small ops/HR layer to keep the team running."
        ),
    }


# ─── Hiring Guide (Groq LLM — NO ML dependency) ───
@app.post("/hiring-guide")
def hiring_guide(body: HiringGuideInput):
    """
    Generates a detailed hiring guide using only Groq LLM.
    Does NOT depend on ml_service at all.
    """
    if SERVICES_AVAILABLE and llm_service:
        try:
            result = llm_service.generate_hiring_guide(
                body.user_input, body.ml_results, body.hierarchy
            )
            return result
        except Exception as e:
            print("Hiring guide LLM error:", e)

    # ── Stub fallback (used when LLM is unavailable) ──
    next_hires = body.hierarchy.get("recommended_next_hires", [
        {"role": "Senior Full-Stack Engineer", "priority": "High",
         "reason": "Core product velocity depends on this hire"},
        {"role": "Product Manager",            "priority": "High",
         "reason": "Without a PM, engineering ships the wrong things"},
    ])

    hiring_profiles = []
    for h in next_hires:
        hiring_profiles.append({
            "role":               h.get("role", "Engineer"),
            "department":         "Engineering" if "engineer" in h.get("role","").lower() else "Product",
            "priority":           h.get("priority", "High"),
            "seniority":          "Mid",
            "experience_years":   "3-5",
            "salary_range":       "$75,000 – $110,000",
            "must_have_skills":   ["Domain expertise", "Communication", "Problem solving", "Teamwork"],
            "nice_to_have_skills":["Startup experience", "Data literacy"],
            "qualifications":     ["Relevant degree or equivalent experience", "2+ years in similar role"],
            "key_responsibilities":[
                f"Own the {h.get('role', 'function')} end-to-end",
                "Collaborate cross-functionally with founders and team leads",
                "Report key metrics and OKRs weekly",
            ],
            "interview_signals":  ["Ownership mindset", "Adaptability", "Clear communication"],
            "why_critical":       h.get("reason", "Critical for current growth stage."),
        })

    return {
        "hiring_profiles": hiring_profiles,
        "hiring_sequence": [
            {"order": i + 1, "role": h.get("role", ""), "rationale": h.get("reason", "")}
            for i, h in enumerate(next_hires)
        ],
        "culture_fit_signals": [
            "Bias for action over perfect planning",
            "Comfort with ambiguity and rapid iteration",
            "Strong written async communication",
        ],
        "onboarding_tips": (
            "Assign a 30-60-90 day plan focused on one quick win per phase. "
            "Pair every new hire with a founder for the first two weeks. "
            "Run a structured onboarding doc review in week one."
        ),
    }


# ─── Industry News ────────────────────────────────
@app.get("/news")
def news(domain: str = Query("SaaS")):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"articles": [], "error": "Missing NEWS_API_KEY"}
    try:
        resp = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": domain, "apiKey": api_key,
                "pageSize": 15, "language": "en", "sortBy": "publishedAt",
            },
        )
        data         = resp.json()
        raw          = data.get("articles", [])
        domain_lower = domain.lower()
        filtered = [
            a for a in raw
            if domain_lower in (a.get("title") or "").lower()
            or domain_lower in (a.get("description") or "").lower()
        ]
        articles = filtered[:8] if filtered else raw[:5]
        normalized = [
            {
                "title":       a.get("title", "No title"),
                "description": a.get("description", ""),
                "url":         a.get("url", "#"),
                "source":      a.get("source", {}).get("name", "Unknown"),
                "published":   a.get("publishedAt", ""),
            }
            for a in articles
            if a.get("title") and "[Removed]" not in a.get("title", "")
        ]
        return {"articles": normalized}
    except Exception as e:
        return {"error": str(e), "articles": []}


# ─── Analytics Dataset ────────────────────────────
# @app.get("/analytics")
# def analytics():
#     try:
#         import pandas as pd
#         csv_path = os.path.join(
#             os.path.dirname(__file__), "..", "data", "synthetic_startups.csv"
#         )
#         if os.path.exists(csv_path):
#             df = pd.read_csv(csv_path)
#             return {"data": df.to_dict(orient="records")}
#     except Exception as e:
#         print("Analytics error:", e)
#     return {"data": []}
# ─── Analytics Dataset ────────────────────────────
@app.get("/analytics")
def analytics():
    try:
        import pandas as pd

        csv_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "synthetic_startups.csv"
        )

        print("CSV PATH:", csv_path)

        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            print("CSV Loaded:", len(df))
            return {"data": df.to_dict(orient="records")}

        print("CSV NOT FOUND")

    except Exception as e:
        print("Analytics error:", e)

    return {"data": []}

# ─── PDF Report ───────────────────────────────────
@app.post("/generate-report")
def generate_report(body: ReportInput):
    try:
        from services.report_service import generate_pdf_report
        buf = generate_pdf_report(body.dict())
        return StreamingResponse(
            buf,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


# ─── Pitch Deck ───────────────────────────────────
@app.post("/generate-pitch")
def generate_pitch(body: PitchInput):
    try:
        from services.pitch_service import generate_pitch_deck
        path = generate_pitch_deck(body.dict())
        with open(path, "rb") as f:
            content = f.read()
        os.remove(path)
        return StreamingResponse(
            BytesIO(content),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": "attachment; filename=bizgenius_pitch.pptx"},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Pitch generation failed: {str(e)}")


# ─── Quick PDF download (test endpoint) ───────────
@app.get("/download/pdf")
def download_pdf():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, "BizGenius Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.save()
    buf.seek(0)
    return StreamingResponse(
        buf, media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=bizgenius_report.pdf"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)