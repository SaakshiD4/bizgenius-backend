import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.classification_model import StartupClassifier
from models.funding_predictor import FundingPredictor
from config import Config


class MLService:
    def __init__(self):
        self.classifier_path    = Config.CLASSIFIER_PATH
        self.funding_model_path = Config.FUNDING_PREDICTOR_PATH
        self.scaler_path        = Config.SCALER_PATH
        self.features_path      = Config.FEATURES_PATH

        self.classifier       = StartupClassifier()
        self.funding_predictor = FundingPredictor()
        self._load_models()

    def _load_models(self):
        try:
            for path in [self.classifier_path, self.funding_model_path,
                         self.scaler_path, self.features_path]:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Model file not found: {path}")

            self.classifier.load(self.classifier_path)
            self.funding_predictor.load(
                self.funding_model_path,
                self.scaler_path,
                self.features_path
            )
            print("✅ All ML models loaded successfully")

        except Exception as e:
            print(f"⚠️ Could not load ML models: {e}")
            print("💡 Run: python models/train_models.py")
            raise

    def predict_startup_risk(self, company_age, founder_count, employees,
                              funding_rounds, funding_per_round, investor_count):
        classification_results = self.classifier.predict(
            company_age, founder_count, employees,
            funding_rounds, funding_per_round, investor_count
        )
        predicted_funding = self.funding_predictor.predict(
            company_age, founder_count, employees,
            funding_rounds, funding_per_round, investor_count
        )
        return {
            "classification":            classification_results["classification"],
            "risk_level":                classification_results["risk_level"],
            "success_probability":       classification_results["success_probability"],
            "probabilities":             classification_results["probabilities"],
            "predicted_funding_usd":     predicted_funding,
            "predicted_funding_formatted": f"${predicted_funding:,.2f}"
        }

    def get_probable_risks(self, user_input, ml_results):
        risks = []

        if ml_results.get("predicted_funding_usd", 0) < 200000:
            risks.append("Insufficient runway / funding to scale")

        if user_input.get("company_age", 0) < 2 and user_input.get("employees", 0) < 10:
            risks.append("Early-stage product/market fit risk")

        if user_input.get("funding_rounds", 0) <= 1:
            risks.append("Limited investor validation")

        domain = user_input.get("domain", "").lower()
        if "fintech" in domain or "finance" in domain:
            risks.append("Regulatory risk (FinTech)")
        elif "health" in domain or "medical" in domain:
            risks.append("Regulatory risk (HealthTech)")

        if ml_results.get("classification") == "Failure":
            risks.append("Similar pattern to failed startups")
        elif ml_results.get("classification") == "Uncertain":
            risks.append("High uncertainty - needs validation")

        if user_input.get("employees", 0) > 0:
            total_funding = user_input.get("funding_rounds", 1) * user_input.get("funding_per_round", 0)
            funding_per_employee = total_funding / user_input.get("employees", 1)
            if funding_per_employee < 10000:
                risks.append("Low funding per employee (burn risk)")

        return risks if risks else ["No significant risks identified"]


ml_service = MLService()