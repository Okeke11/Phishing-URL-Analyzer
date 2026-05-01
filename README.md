# 🛡️ Intelligent Phishing URL Analyzer

An AI-powered backend API that analyzes URLs in real-time to detect phishing attempts. Instead of relying on static blacklists, this system extracts lexical features from the URL and uses a Machine Learning model to predict malicious intent.

## ✨ Features
* **Behavioral Analysis:** Extracts URL characteristics (length, raw IPs, subdomain counts, suspicious keywords) to evaluate risk.
* **Machine Learning Engine:** Powered by a Random Forest Classifier trained on a dataset of over 50,000 legitimate and malicious URLs.
* **High-Speed API:** Built with FastAPI for lightning-fast, asynchronous response times.
* **Fault-Tolerant:** Includes robust error handling to process malformed or obfuscated URLs without crashing.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
* **API Framework:** FastAPI, Uvicorn
* **Environment:** Windows / PowerShell

## 🚀 Installation & Setup (Windows)

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/YourUsername/phishing-analyzer.git
   cd phishing-analyzer
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install fastapi uvicorn scikit-learn pandas numpy joblib
   ```

4. **Train the Model (Optional):**  
   *(Note: You need to download a phishing dataset CSV and place it in the root directory to train from scratch.)*
   ```powershell
   python train_model.py
   ```

5. **Run the API Server:**
   ```powershell
   uvicorn main:app --reload
   ```

---

## 🔌 API Usage

Once the server is running, navigate to:

http://127.0.0.1:8000/docs

Use the interactive Swagger UI or make a POST request directly.

### **Endpoint:**  
`POST /analyze`

### **Request Body (JSON):**
```json
{
  "url": "http://192.168.1.55/secure-update/verify-account"
}
```

### **Response:**
```json
{
  "url": "http://192.168.1.55/secure-update/verify-account",
  "is_phishing": true,
  "risk_score_percent": 87.5,
  "features_extracted": {
    "url_length": 48,
    "has_ip": 1,
    "dot_count": 3,
    "is_https": 0,
    "has_suspicious_word": 1,
    "has_at_symbol": 0
  }
}
```

---

## 🔮 Future Improvements

- [ ] Advanced Feature Extraction  
  - Detect URL shorteners (e.g., bit.ly)  
  - Shannon entropy (character randomness)  
  - Hyphen analysis  

- [ ] Frontend Dashboard  
  - Build a clean React or Vanilla JS interface  
  - Visualize risk scores  

- [ ] Dockerization  
  - Containerize the application for seamless deployment  
