
# Use a pipeline as a high-level helper
from transformers import pipeline

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ko-en")
result = translator("This is a test sentence.")
print(result[0]["translation_text"])
