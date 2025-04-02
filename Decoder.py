from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-base-seq2seq")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-base-seq2seq")

# Prepare GODEL-style input
instruction = "Instruction: Respond to the user in a friendly and helpful way."
context = "Context: The user asked for a book recommendation."
knowledge = "Knowledge: I recommend 'The Hobbit' by J.R.R. Tolkien."

# Combine into one input string
input_text = f"{instruction} {context} {knowledge}"

# Tokenize and generate
inputs = tokenizer(input_text, return_tensors="pt")
generated_ids = model.generate(**inputs, max_length=60, do_sample=True)
response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

print("GODEL:", response)
