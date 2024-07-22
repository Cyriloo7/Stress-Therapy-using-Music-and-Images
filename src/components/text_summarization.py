from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


inputs = tokenizer(text, max_length=8192, return_tensors="pt")

max_token_id = inputs['input_ids'].max().item()
vocab_size = tokenizer.vocab_size
if max_token_id >= vocab_size:
     return jsonify({'error': f'Token ID {max_token_id} exceeds vocabulary size of {vocab_size}'})
attention_mask = inputs.attention_mask
inputs = inputs.to(device)
attention_mask = attention_mask.to(device)
