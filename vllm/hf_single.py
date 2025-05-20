import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")
model = AutoModelForCausalLM.from_pretrained("facebook/opt-125m").cuda()
model.eval()

prompt = "Explain the significance of the theory of relativity in modern physics."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

start = time.time()
with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=100)
ttft = time.time()
text = tokenizer.decode(output[0], skip_special_tokens=True)
end = time.time()

tokens_generated = len(text.split())

print("=== HF Single Request Benchmark ===")
print(f"TTFT: {ttft - start:.4f} sec")
print(f"Total Latency: {end - start:.4f} sec")
print(f"Tokens Generated: {tokens_generated}")
print(f"Tokens/sec: {tokens_generated / (end - start):.2f}")
