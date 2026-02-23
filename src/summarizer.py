from transformers import pipeline
from .utils import clean_text, chunk_text

# Load model once to avoid reloading (global variable for simplicity in this script)
# In production, we might use a class or caching.
summarizer_pipeline = None

def load_summarizer_model():
    """
    Loads the T5-small summarization pipeline.
    This runs offline after the first download.
    """
    global summarizer_pipeline
    if summarizer_pipeline is None:
        print("Loading T5-small model...")
        # 't5-small' is very lightweight (~240MB) and good for CPU.
        summarizer_pipeline = pipeline("summarization", model="t5-small", device=-1) # device=-1 forces CPU
    return summarizer_pipeline

def generate_summary(text):
    """
    Main function to generate summary from text.
    Handles chunking for long texts.
    """
    if not text:
        return "No text provided to summarize."

    # 1. Clean Text
    cleaned_text = clean_text(text)
    
    # 2. Chunk Text (T5 has a limit, usually 512 tokens)
    chunks = chunk_text(cleaned_text)
    
    # 3. Summarize each chunk
    summarizer = load_summarizer_model()
    summaries = []
    
    print(f"Summarizing {len(chunks)} chunks...")
    for chunk in chunks:
        # T5 expects "summarize: " prefix
        input_text = "summarize: " + chunk
        
        # Determine max_length mainly based on input length but capped
        input_len = len(input_text.split())
        max_len = min(150, max(30, int(input_len * 0.5)))
        min_len = 10
        
        try:
            # clean_up_tokenization_spaces=True avoids some warnings
            res = summarizer(input_text, max_length=max_len, min_length=min_len, do_sample=False)
            summary_text = res[0]['summary_text']
            summaries.append(summary_text)
        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            
    # 4. Combine Summaries
    final_summary = " ".join(summaries)
    
    return final_summary
