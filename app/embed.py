from transformers import AutoTokenizer, AutoModel
import torch


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# texts = ["Hello world!", "How are you today?"]
batchs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

with torch.no_grad():
    outputs = model(**batchs)

embeddings = outputs.last_hidden_state.mean(dim=1)

print(embeddings.shape)