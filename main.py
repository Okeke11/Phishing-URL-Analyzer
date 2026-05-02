from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # <-- ADD THIS
from pydantic import BaseModel
import joblib
import pandas as pd
from feature_extractor import extract_url_features

print("Loading Machine Learning Model...")
model = joblib.load("phishing_model_pro.pkl")

app = FastAPI(title="Phishing URL Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

# --- CHANGE YOUR ROOT ROUTE TO THIS ---
@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.post("/analyze")
def analyze_url(request: URLRequest):
    features = extract_url_features(request.url)
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)[0]
    probabilities = model.predict_proba(features_df)[0]
    risk_score = round(probabilities[1] * 100, 2)
    
    return {
        "url": request.url,
        "is_phishing": bool(prediction == 1),
        "risk_score_percent": risk_score,
        "features_extracted": features
    }