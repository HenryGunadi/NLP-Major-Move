import re

def safe_get(data, key, default=None):
    return data .get(key, default) if isinstance(data, dict) else default

def clean_text(text):
    if text is None:
        return text

    text = re.sub(r"<.*?>", "", text) # remove HTML tags
    text = re.sub(r"\s+", " ", text).strip() # normalize spaces
    text = re.sub(r"(.)\1{2,}", r"\1\1", text) # limit repeated chars
    return text