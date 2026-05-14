# import pandas as pd
# import numpy as np
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.preprocessing import RobustScaler
# from sklearn.model_selection import train_test_split
# import pickle
# import os

# class FundingPredictor:
#     def __init__(self):
#         self.model = None
#         self.scaler = None
#         self.regression_features = None
    
#     def train(self, dataset_path):
#         """Train the funding prediction model"""
#         print("🔄 Training Funding Predictor Model...")
        
#         # Load dataset
#         df = pd.read_csv(dataset_path, encoding="latin1")
        
#         # Base features
#         features = ["company_age_years", "founder_count", "employees_size_numeric",
#                    "funding_rounds", "funding_per_round", "investor_count"]
        
#         # Convert to numeric
#         for col in features:
#             df[col] = pd.to_numeric(df[col], errors="coerce")
        
#         # Handle missing values
#         df['employees_size_numeric'].fillna(df['employees_size_numeric'].median(), inplace=True)
#         df['founder_count'].fillna(2, inplace=True)
#         df['investor_count'].fillna(df['funding_rounds'], inplace=True)
#         df['employees_size_numeric'] = df['employees_size_numeric'].replace(0, 5)
#         df['company_age_years'] = df['company_age_years'].replace(0, 0.5)
#         df[features] = df[features].fillna(0)
        
#         # Calculate Total Funding
#         if 'total_funding_usd' in df.columns:
#             df['total_funding'] = pd.to_numeric(df['total_funding_usd'], errors='coerce')
#         else:
#             df['total_funding'] = df['funding_rounds'] * df['funding_per_round']
        
#         df = df[df['total_funding'] > 0]
#         df = df[df['total_funding'] < 1e12]
        
#         # Feature Engineering
#         df['funding_rounds'] = df['funding_rounds'].replace(0, 1)
#         df['investor_count'] = df['investor_count'].replace(0, 1)
        
#         df['funding_efficiency'] = df['total_funding'] / df['funding_rounds']
#         df['funding_per_employee'] = df['total_funding'] / df['employees_size_numeric']
#         df['investor_per_round'] = df['investor_count'] / df['funding_rounds']
#         df['employee_growth_rate'] = df['employees_size_numeric'] / df['company_age_years']
#         df['rounds_per_year'] = df['funding_rounds'] / df['company_age_years']
        
#         self.regression_features = features + [
#             'funding_efficiency', 'funding_per_employee', 'investor_per_round',
#             'employee_growth_rate', 'rounds_per_year'
#         ]
        
#         # Clean data
#         df[self.regression_features] = df[self.regression_features].replace([np.inf, -np.inf], np.nan)
#         for col in self.regression_features:
#             if df[col].isna().any():
#                 median_val = df[col].median()
#                 if np.isnan(median_val):
#                     median_val = 0
#                 df[col].fillna(median_val, inplace=True)
        
#         df = df.dropna(subset=self.regression_features + ['total_funding'])
        
#         # Target: Next round funding (average funding per round)
#         df['next_round_funding'] = df['funding_per_round']
        
#         # Prepare data
#         X = df[self.regression_features].values
#         y = df['next_round_funding'].values
        
#         # Remove invalid data
#         mask = ~(np.isnan(X).any(axis=1) | np.isinf(X).any(axis=1) |
#                 np.isnan(y) | np.isinf(y) | (y <= 0))
#         X = X[mask]
#         y = y[mask]
        
#         # Log transform
#         y_log = np.log10(y)
        
#         # Scale features
#         self.scaler = RobustScaler()
#         X_scaled = self.scaler.fit_transform(X)
        
#         # Train-test split
#         X_train, X_test, y_train_log, y_test_log = train_test_split(
#             X_scaled, y_log, test_size=0.2, random_state=42
#         )
        
#         # Train model
#         self.model = GradientBoostingRegressor(
#             n_estimators=200,
#             max_depth=6,
#             learning_rate=0.1,
#             subsample=0.8,
#             random_state=42
#         )
        
#         self.model.fit(X_train, y_train_log)
        
#         # Evaluate
#         y_test_pred_log = self.model.predict(X_test)
#         y_test_actual = 10 ** y_test_log
#         y_test_pred = 10 ** y_test_pred_log
        
#         from sklearn.metrics import r2_score
#         r2 = r2_score(y_test_actual, y_test_pred)
        
#         print(f"✅ Model Trained! R² Score: {r2:.2%}")
#         return r2
    
#     def save(self, model_path, scaler_path, features_path):
#         """Save model, scaler, and features"""
#         os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
#         with open(model_path, 'wb') as f:
#             pickle.dump(self.model, f)
#         with open(scaler_path, 'wb') as f:
#             pickle.dump(self.scaler, f)
#         with open(features_path, 'wb') as f:
#             pickle.dump(self.regression_features, f)
        
#         print(f"💾 Models saved successfully")
    
#     def load(self, model_path, scaler_path, features_path):
#         """Load model, scaler, and features"""
#         with open(model_path, 'rb') as f:
#             self.model = pickle.load(f)
#         with open(scaler_path, 'rb') as f:
#             self.scaler = pickle.load(f)
#         with open(features_path, 'rb') as f:
#             self.regression_features = pickle.load(f)
        
#         print(f"✅ Models loaded successfully")
    
#     def predict(self, company_age, founder_count, employees,
#                 funding_rounds, funding_per_round, investor_count):
#         """
#         Predict next round funding
        
#         Returns:
#             float - Predicted next round funding in USD
#         """
#         if self.model is None or self.scaler is None:
#             raise ValueError("Model not loaded. Call load() first.")
        
#         # Safety checks
#         employees = max(employees, 5)
#         company_age = max(company_age, 0.5)
#         funding_rounds = max(funding_rounds, 1)
#         investor_count = max(investor_count, 1)
        
#         total_raised = funding_rounds * funding_per_round
        
#         # Build features
#         features_dict = {
#             'company_age_years': company_age,
#             'founder_count': founder_count,
#             'employees_size_numeric': employees,
#             'funding_rounds': funding_rounds,
#             'funding_per_round': funding_per_round,
#             'investor_count': investor_count,
#             'funding_efficiency': total_raised / funding_rounds,
#             'funding_per_employee': total_raised / employees,
#             'investor_per_round': investor_count / funding_rounds,
#             'employee_growth_rate': employees / company_age,
#             'rounds_per_year': funding_rounds / company_age
#         }
        
#         # Create array
#         features_array = np.array([[features_dict[f] for f in self.regression_features]])
        
#         # Scale and predict
#         features_scaled = self.scaler.transform(features_array)
#         pred_log = self.model.predict(features_scaled)
#         next_round_funding = 10 ** pred_log[0]
        
#         return float(next_round_funding)
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
import pickle
import os

class FundingPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.regression_features = None
    
    def train(self, dataset_path):
        print("🔄 Training Funding Predictor Model...")
        df = pd.read_csv(dataset_path, encoding="latin1")

        features = ["company_age_years", "founder_count", "employees_size_numeric",
                    "funding_rounds", "funding_per_round", "investor_count"]

        for col in features:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df['employees_size_numeric'].fillna(df['employees_size_numeric'].median(), inplace=True)
        df['founder_count'].fillna(2, inplace=True)
        df['investor_count'].fillna(df['funding_rounds'], inplace=True)
        df['employees_size_numeric'] = df['employees_size_numeric'].replace(0, 5)
        df['company_age_years'] = df['company_age_years'].replace(0, 0.5)
        df[features] = df[features].fillna(0)

        if 'total_funding_usd' in df.columns:
            df['total_funding'] = pd.to_numeric(df['total_funding_usd'], errors='coerce')
        else:
            df['total_funding'] = df['funding_rounds'] * df['funding_per_round']

        df = df[df['total_funding'] > 0]
        df = df[df['total_funding'] < 1e12]

        df['funding_rounds'] = df['funding_rounds'].replace(0, 1)
        df['investor_count'] = df['investor_count'].replace(0, 1)

        df['funding_efficiency'] = df['total_funding'] / df['funding_rounds']
        df['funding_per_employee'] = df['total_funding'] / df['employees_size_numeric']
        df['investor_per_round'] = df['investor_count'] / df['funding_rounds']
        df['employee_growth_rate'] = df['employees_size_numeric'] / df['company_age_years']
        df['rounds_per_year'] = df['funding_rounds'] / df['company_age_years']

        self.regression_features = features + [
            'funding_efficiency', 'funding_per_employee', 'investor_per_round',
            'employee_growth_rate', 'rounds_per_year'
        ]

        df[self.regression_features] = df[self.regression_features].replace([np.inf, -np.inf], np.nan)
        for col in self.regression_features:
            median_val = df[col].median()
            df[col].fillna(median_val if not np.isnan(median_val) else 0, inplace=True)

        df = df.dropna(subset=self.regression_features + ['total_funding'])
        df['next_round_funding'] = df['funding_per_round']

        X = df[self.regression_features].values
        y = df['next_round_funding'].values
        mask = ~(np.isnan(X).any(axis=1) | np.isinf(X).any(axis=1) |
                 np.isnan(y) | np.isinf(y) | (y <= 0))
        X = X[mask]
        y = y[mask]

        y_log = np.log10(y)
        self.scaler = RobustScaler()
        X_scaled = self.scaler.fit_transform(X)

        X_train, X_test, y_train_log, y_test_log = train_test_split(
            X_scaled, y_log, test_size=0.2, random_state=42
        )

        self.model = GradientBoostingRegressor(
            n_estimators=200, max_depth=6, learning_rate=0.1,
            subsample=0.8, random_state=42
        )

        self.model.fit(X_train, y_train_log)
        y_test_pred_log = self.model.predict(X_test)
        y_test_actual = 10 ** y_test_log
        y_test_pred = 10 ** y_test_pred_log

        from sklearn.metrics import r2_score
        r2 = r2_score(y_test_actual, y_test_pred)
        print(f"✅ Model Trained! R² Score: {r2:.2%}")
        return r2

    def save(self, model_path, scaler_path, features_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        with open(features_path, 'wb') as f:
            pickle.dump(self.regression_features, f)
        print("💾 Models saved successfully")

    def load(self, model_path, scaler_path, features_path):
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        with open(features_path, 'rb') as f:
            self.regression_features = pickle.load(f)
        print("✅ Models loaded successfully")

    def predict(self, company_age, founder_count, employees,
                funding_rounds, funding_per_round, investor_count):
        if self.model is None or self.scaler is None:
            raise ValueError("Model not loaded. Call load() first.")
        employees = max(employees, 5)
        company_age = max(company_age, 0.5)
        funding_rounds = max(funding_rounds, 1)
        investor_count = max(investor_count, 1)

        total_raised = funding_rounds * funding_per_round
        features_dict = {
            'company_age_years': company_age,
            'founder_count': founder_count,
            'employees_size_numeric': employees,
            'funding_rounds': funding_rounds,
            'funding_per_round': funding_per_round,
            'investor_count': investor_count,
            'funding_efficiency': total_raised / funding_rounds,
            'funding_per_employee': total_raised / employees,
            'investor_per_round': investor_count / funding_rounds,
            'employee_growth_rate': employees / company_age,
            'rounds_per_year': funding_rounds / company_age
        }

        features_array = np.array([[features_dict[f] for f in self.regression_features]])
        features_scaled = self.scaler.transform(features_array)
        pred_log = self.model.predict(features_scaled)
        next_round_funding = 10 ** pred_log[0]
        return float(next_round_funding)
