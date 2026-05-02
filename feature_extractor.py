import re
import math
from urllib.parse import urlparse

def calculate_entropy(string: str) -> float:
    """Calculates the Shannon entropy of a string to detect random, machine-generated domains."""
    if not string:
        return 0
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = - sum(p * math.log2(p) for p in prob)
    return entropy

def extract_url_features(url) -> dict:
    """
    Parses a raw URL and extracts advanced numerical/boolean features for ML classification.
    """
    features = {}
    url_str = str(url).strip()
    
    # 1. Base Features
    features['url_length'] = len(url_str)
    
    if not url_str.startswith('http'):
        url_str = 'http://' + url_str
        
    # 2. Structural & Obfuscation Features
    try:
        parsed_url = urlparse(url_str)
        features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', parsed_url.netloc) else 0
        features['dot_count'] = parsed_url.netloc.count('.')
        features['is_https'] = 1 if parsed_url.scheme == 'https' else 0
    except ValueError:
        features['has_ip'] = 0
        features['dot_count'] = 0
        features['is_https'] = 0
    
    # 3. Lexical Analysis
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm', 'invoice', 'auth']
    features['has_suspicious_word'] = 1 if any(word in url_str.lower() for word in suspicious_words) else 0
    features['has_at_symbol'] = 1 if '@' in url_str else 0
    
    # --- 🚀 THE UPGRADES ---
    
    # 4. Math/Randomness Analysis
    features['entropy'] = calculate_entropy(url_str)
    
    # 5. Typographical Analysis
    features['num_hyphens'] = url_str.count('-')
    features['num_digits'] = sum(c.isdigit() for c in url_str)
    
    # 6. Service Obfuscation Analysis
    shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'is.gd', 'cli.gs', 'yfrog.com', 'cutt.ly']
    features['is_shortened'] = 1 if any(short in url_str.lower() for short in shorteners) else 0
    
    return features