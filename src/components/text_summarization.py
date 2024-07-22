from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("Azma-AI/bart-large-text-summarizer")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForSeq2SeqLM.from_pretrained("Azma-AI/bart-large-text-summarizer")
model = model.to(device)

inputs = tokenizer(text, max_length=8192, return_tensors="pt")

max_token_id = inputs['input_ids'].max().item()
vocab_size = tokenizer.vocab_size
if max_token_id >= vocab_size:
     return jsonify({'error': f'Token ID {max_token_id} exceeds vocabulary size of {vocab_size}'})
attention_mask = inputs.attention_mask
inputs = inputs.to(device)
attention_mask = attention_mask.to(device)

# Generate Summary
summary_ids = model.generate(inputs["input_ids"], min_length=150, max_length=512, attention_mask=attention_mask)
decoded_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)