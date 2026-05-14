# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#     NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#     GROQ_MODEL   = "llama3-8b-8192"

#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#     MODELS_DIR             = os.path.join(BASE_DIR, "models", "saved_models")
#     CLASSIFIER_PATH        = os.path.join(MODELS_DIR, "startup_classifier.pkl")
#     FUNDING_PREDICTOR_PATH = os.path.join(MODELS_DIR, "next_round_predictor.pkl")
#     SCALER_PATH            = os.path.join(MODELS_DIR, "scaler_next_round.pkl")
#     FEATURES_PATH          = os.path.join(MODELS_DIR, "features_next_round.pkl")

#     CHROMA_DIR = os.path.join(BASE_DIR, "..", "chroma_db")
#     DATA_DIR   = os.path.join(BASE_DIR, "..", "data")

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    GROQ_MODEL   = "llama-3.1-8b-instant"   

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MODELS_DIR             = os.path.join(BASE_DIR, "models", "saved_models")
    CLASSIFIER_PATH        = os.path.join(MODELS_DIR, "startup_classifier.pkl")
    FUNDING_PREDICTOR_PATH = os.path.join(MODELS_DIR, "next_round_predictor.pkl")
    SCALER_PATH            = os.path.join(MODELS_DIR, "scaler_next_round.pkl")
    FEATURES_PATH          = os.path.join(MODELS_DIR, "features_next_round.pkl")

    # CHROMA_DIR = os.path.join(BASE_DIR, "..", "chroma_db")
    # DATA_DIR   = os.path.join(BASE_DIR, "..", "data")
    CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
    DATA_DIR   = os.path.join(BASE_DIR, "data")