from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

print("Loading Hugging Face model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Model loaded successfully!")

# English to Tamil
tokenizer.src_lang = "eng_Latn"

text = "Hello, how are you?"

inputs = tokenizer(text, return_tensors="pt")

translated_tokens = model.generate(
    **inputs,
    forced_bos_token_id=tokenizer.convert_tokens_to_ids("tam_Taml"),
    max_length=128
)

translation = tokenizer.batch_decode(
    translated_tokens,
    skip_special_tokens=True
)[0]

print("\nEnglish:", text)
print("Tamil:", translation)