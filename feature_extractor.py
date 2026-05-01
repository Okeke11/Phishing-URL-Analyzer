import re
from urllib.parse import urlparse

def extract_url_features(url) -> dict:
    """
    Parses a raw URL and extracts numerical/boolean features for ML classification.
    """
    features = {}
    
    # 1. Length Features (Cast to string in case of empty rows/NaN values)
    url_str = str(url)
    features['url_length'] = len(url_str)
    
    # Ensure URL has a scheme for proper parsing
    if not url_str.startswith('http'):
        url_str = 'http://' + url_str
        
    # 2 & 3. Structural & Security Features (Protected against malformed URLs)
    try:
        parsed_url = urlparse(url_str)
        
        # Phishers often use raw IPs to hide their origin
        features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', parsed_url.netloc) else 0
        
        # Excessive subdomains
        features['dot_count'] = parsed_url.netloc.count('.')
        
        # Security Protocol
        features['is_https'] = 1 if parsed_url.scheme == 'https' else 0
        
    except ValueError:
        # If the URL is so mangled that urlparse crashes (like bad IPv6 formats),
        # we assign default 0s instead of crashing the entire script.
        features['has_ip'] = 0
        features['dot_count'] = 0
        features['is_https'] = 0
    
    # 4. Lexical Analysis (Suspicious Keywords) - runs safely on the raw string
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm']
    features['has_suspicious_word'] = 1 if any(word in url_str.lower() for word in suspicious_words) else 0
    
    # 5. Obfuscation Techniques
    features['has_at_symbol'] = 1 if '@' in url_str else 0
    
    return features