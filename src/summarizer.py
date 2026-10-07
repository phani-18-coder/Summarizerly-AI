import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from .utils import clean_text, chunk_text

# Force PyTorch backend, avoid TF/Keras conflicts
import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

_model = None
_tokenizer = None

def load_summarizer_model():
    """
    Loads T5-small model and tokenizer explicitly with PyTorch.
    Bypasses the pipeline to avoid Keras 3.x conflicts.
    """
    global _model, _tokenizer
    if _model is None:
        print("Loading T5-small model...")
        _tokenizer = T5Tokenizer.from_pretrained("t5-small")
        _model = T5ForConditionalGeneration.from_pretrained("t5-small")
        _model.eval()
    return _model, _tokenizer

def generate_summary(text):
    """
    Generates summary from text using T5-small with PyTorch directly.
    Handles chunking for long texts.
    """
    if not text:
        return "No text provided to summarize."

    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)

    model, tokenizer = load_summarizer_model()
    summaries = []

    print(f"Summarizing {len(chunks)} chunk(s)...")
    for chunk in chunks:
        input_text = "summarize: " + chunk

        inputs = tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        input_len = inputs.shape[1]
        max_len = min(150, max(30, int(input_len * 0.5)))

        try:
            with torch.no_grad():
                output_ids = model.generate(
                    inputs,
                    max_length=max_len,
                    min_length=10,
                    num_beams=4,
                    early_stopping=True
                )
            summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            summaries.append(summary)
        except Exception as e:
            print(f"Error summarizing chunk: {e}")

    return " ".join(summaries)
