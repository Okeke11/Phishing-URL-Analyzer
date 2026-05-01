from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from feature_extractor import extract_url_features

print("Loading Machine Learning Model...")
# Load the brain we just trained
model = joblib.load("phishing_model_pro.pkl")

# Initialize the API
app = FastAPI(title="Phishing URL Analyzer API", description="AI-powered phishing detection.")

# Define the expected JSON format for incoming requests
class URLRequest(BaseModel):
    url: str

@app.post("/analyze")
def analyze_url(request: URLRequest):
    # 1. Extract features using the exact same logic used during training
    features = extract_url_features(request.url)
    
    # 2. Convert to DataFrame (Scikit-Learn expects 2D data structures)
    features_df = pd.DataFrame([features])
    
    # 3. Ask the model to predict (0 = Safe, 1 = Phishing)
    prediction = model.predict(features_df)[0]
    
    # 4. Get the confidence/probability scores
    probabilities = model.predict_proba(features_df)[0]
    risk_score = round(probabilities[1] * 100, 2)
    
    return {
        "url": request.url,
        "is_phishing": bool(prediction == 1),
        "risk_score_percent": risk_score,
        "features_extracted": features
    }