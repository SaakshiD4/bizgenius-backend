# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from imblearn.over_sampling import SMOTE
# import pickle
# import os

# class StartupClassifier:
#     def __init__(self):
#         self.model = None
#         self.features = ["company_age_years", "founder_count", "employees_size_numeric",
#                         "funding_rounds", "funding_per_round", "investor_count"]
#         self.label_mapping = {0: "Uncertain", 1: "Failure", 2: "Success"}
#         self.reverse_mapping = {-1: 0, 0: 1, 1: 2}
    
#     def train(self, dataset_path):
#         """Train the classification model"""
#         print("🔄 Training Classification Model...")
        
#         # Load dataset
#         df = pd.read_csv(dataset_path, encoding="latin1")
        
#         # Ensure numeric columns
#         for col in self.features:
#             df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        
#         # Map labels -1,0,1 → 0,1,2
#         df["label_mapped"] = df["label"].map(self.reverse_mapping)
        
#         # Split features & target
#         X = df[self.features]
#         y = df["label_mapped"]
        
#         # Apply SMOTE to balance classes
#         smote = SMOTE(random_state=42)
#         X_res, y_res = smote.fit_resample(X, y)
        
#         # Train-test split
#         X_train, X_test, y_train, y_test = train_test_split(
#             X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
#         )
        
#         # Train Random Forest
#         self.model = RandomForestClassifier(
#             n_estimators=200,
#             max_depth=10,
#             random_state=42,
#             class_weight='balanced_subsample',
#             n_jobs=-1
#         )
#         self.model.fit(X_train, y_train)
        
#         # Evaluate
#         y_pred = model.predict(X_test)
#         accuracy = (y_pred == y_test).mean()
        
#         print(f"✅ Model Trained! Accuracy: {accuracy:.2%}")
#         return accuracy
    
#     def save(self, filepath):
#         """Save the trained model"""
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
#         with open(filepath, 'wb') as f:
#             pickle.dump(self.model, f)
#         print(f"💾 Model saved to {filepath}")
    
#     def load(self, filepath):
#         """Load a trained model"""
#         with open(filepath, 'rb') as f:
#             self.model = pickle.load(f)
#         print(f"✅ Model loaded from {filepath}")
    
#     def predict(self, company_age, founder_count, employees, 
#                 funding_rounds, funding_per_round, investor_count):
#         """
#         Predict startup success classification
        
#         Returns:
#             dict with classification, probabilities, and risk_level
#         """
#         if self.model is None:
#             raise ValueError("Model not loaded. Call load() first.")
        
#         # Prepare input
#         input_data = np.array([[
#             company_age, founder_count, employees,
#             funding_rounds, funding_per_round, investor_count
#         ]])
        
#         # Predict
#         prediction = self.model.predict(input_data)[0]
#         probabilities = self.model.predict_proba(input_data)[0]
        
#         # Get classification label
#         classification = self.label_mapping[prediction]
        
#         # Calculate risk level
#         success_prob = probabilities[2]  # Probability of success (class 2)
#         if success_prob >= 0.7:
#             risk_level = "Low"
#         elif success_prob >= 0.4:
#             risk_level = "Medium"
#         else:
#             risk_level = "High"
        
#         return {
#             "classification": classification,
#             "probabilities": {
#                 "uncertain": float(probabilities[0]),
#                 "failure": float(probabilities[1]),
#                 "success": float(probabilities[2])
#             },
#             "success_probability": float(success_prob),
#             "risk_level": risk_level
#         }
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import pickle
import os

class StartupClassifier:
    def __init__(self):
        self.model = None
        self.features = [
            "company_age_years", "founder_count", "employees_size_numeric",
            "funding_rounds", "funding_per_round", "investor_count"
        ]
        self.label_mapping = {0: "Uncertain", 1: "Failure", 2: "Success"}
        self.reverse_mapping = {-1: 0, 0: 1, 1: 2}
    
    def train(self, dataset_path):
        """Train the classification model"""
        print("🔄 Training Classification Model...")
        
        # Load dataset
        df = pd.read_csv(dataset_path, encoding="latin1")
        
        # Ensure numeric columns
        for col in self.features:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        
        # Map labels -1,0,1 → 0,1,2
        df["label_mapped"] = df["label"].map(self.reverse_mapping)
        
        # Split features & target
        X = df[self.features]
        y = df["label_mapped"]
        
        # Apply SMOTE to balance classes
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
        )
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            class_weight='balanced_subsample',
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = (y_pred == y_test).mean()
        
        print(f"✅ Model Trained! Accuracy: {accuracy:.2%}")
        return accuracy
    
    def save(self, filepath):
        """Save the trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 Model saved to {filepath}")
    
    def load(self, filepath):
        """Load a trained model"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✅ Model loaded from {filepath}")
    
    def predict(self, company_age, founder_count, employees, 
                funding_rounds, funding_per_round, investor_count):
        """
        Predict startup success classification
        
        Returns:
            dict with classification, probabilities, and risk_level
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load() first.")
        
        # Prepare input
        input_data = np.array([[company_age, founder_count, employees,
                                funding_rounds, funding_per_round, investor_count]])
        
        # Predict
        prediction = self.model.predict(input_data)[0]
        probabilities = self.model.predict_proba(input_data)[0]
        
        # Get classification label
        classification = self.label_mapping[prediction]
        
        # Calculate risk level
        success_prob = probabilities[2]  # Probability of success (class 2)
        if success_prob >= 0.7:
            risk_level = "Low"
        elif success_prob >= 0.4:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "classification": classification,
            "probabilities": {
                "uncertain": float(probabilities[0]),
                "failure": float(probabilities[1]),
                "success": float(probabilities[2])
            },
            "success_probability": float(success_prob),
            "risk_level": risk_level
        }
