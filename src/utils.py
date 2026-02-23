import re

def clean_text(text):
    """
    Cleans the input text by removing excessive whitespace and special characters.
    Good for Viva: "We normalize text to ensure the model focuses on content, not formatting noise."
    """
    if not text:
        return ""
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, max_tokens=512):
    """
    Splits large text into smaller chunks that fit into the model's context window.
    Crucial for T5-small which has a token limit.
    
    Strategy: Split by sentences or fixed characters to respect model limits.
    Simple approach: Character-based chunking with overlap (approx 2000 chars ~ 400-500 tokens).
    """
    # Simple heuristic: 1 token ~= 4 characters. 512 tokens ~= 2048 chars.
    # We use a safe limit of 1500 chars to be sure.
    chunk_size = 1500
    chunks = []
    
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
        
    return chunks
