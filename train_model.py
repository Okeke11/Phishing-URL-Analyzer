import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Import your custom feature extractor
from feature_extractor import extract_url_features

print("1. Loading dataset from CSV...")
try:
    # Assuming your file is named dataset.csv
    df = pd.read_csv("dataset.csv") 
except FileNotFoundError:
    print("Error: Could not find 'dataset.csv'. Make sure it's in the phishing-analyzer folder!")
    exit()

# Let's check the actual column names in case they are capitalized differently
# Typically, they are 'URL' and 'Label'
url_col = df.columns[0]  # Grab the first column dynamically
label_col = df.columns[1] # Grab the second column dynamically

# Map the text labels to binary (0 = Good/Safe, 1 = Bad/Phishing)
print("Translating 'Good' and 'Bad' labels into binary...")
df['is_phishing'] = df[label_col].map({'good': 0, 'bad': 1, 'Good': 0, 'Bad': 1})

# Drop any rows where the mapping failed (just to be safe)
df = df.dropna(subset=['is_phishing'])

# Sample 50,000 rows for a fast but highly accurate test run
# Once you know it works, you can comment these two lines out to train on all 549,346!
if len(df) > 50000:
    print("Sampling 50,000 rows to keep training time reasonable...")
    df = df.sample(n=50000, random_state=42)

print("2. Extracting features from URLs (this will take a minute or two)...")
features_list = df[url_col].apply(extract_url_features).tolist()

X = pd.DataFrame(features_list)
y = df['is_phishing'] 

# 3. Split data into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("3. Training the Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("4. Evaluating Model Accuracy...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%\n")
print("Detailed Report:")
print(classification_report(y_test, y_pred))

# 5. Save the upgraded model
joblib.dump(model, "phishing_model_pro.pkl")
print("Success! Pro model saved as 'phishing_model_pro.pkl'.")