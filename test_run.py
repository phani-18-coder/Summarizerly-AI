from src.summarizer import generate_summary
from src.utils import clean_text, chunk_text

print("--- Starting Verification ---")

# Test Data
long_text = """
Artificial intelligence (AI) is intelligence - perceiving, synthesizing, and inferring information - demonstrated by machines, as opposed to intelligence displayed by non-human animals and humans. Example tasks in which this is done include speech recognition, computer vision, translation between (natural) languages, as well as other mappings of inputs.
AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go).
As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding (known as an "AI winter"), followed by new approaches, success and renewed funding. AI research has tried and discarded many different approaches during its lifetime, including simulating the brain, modeling human problem solving, formal logic, large databases of knowledge and imitating animal behavior. In the first decades of the 21st century, highly mathematical-statistical machine learning has dominated the field, and this technique has proved highly successful, helping to solve many challenging problems throughout industry and academia.
"""

print(f"Original Text Length: {len(long_text)} chars")

# 1. Test Cleaning
cleaned = clean_text(long_text)
print("Text Cleaned.")

# 2. Test Chunking
chunks = chunk_text(cleaned)
print(f"Text Chunked into {len(chunks)} parts.")

# 3. Test Summarization
print("Generating Summary... (This downloads the model if first time, so wait...)")
try:
    summary = generate_summary(cleaned)
    print("\n--- SUMMARY GENERATED ---")
    print(summary)
    print("------------------------")
except Exception as e:
    print(f"Summary failed: {e}")

print("Verification Complete.")
