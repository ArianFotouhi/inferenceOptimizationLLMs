import time
from vllm import LLM, SamplingParams

llm = LLM(model="facebook/opt-125m")
sampling_params = SamplingParams(max_tokens=100)

prompt = "Explain the significance of the theory of relativity in modern physics."

start = time.time()
outputs = llm.generate([prompt], sampling_params)
ttft = time.time()
text = outputs[0].outputs[0].text
end = time.time()

tokens_generated = len(text.split())

print("=== vLLM Single Request Benchmark ===")
print(f"TTFT: {ttft - start:.4f} sec")
print(f"Total Latency: {end - start:.4f} sec")
print(f"Tokens Generated: {tokens_generated}")
print(f"Tokens/sec: {tokens_generated / (end - start):.2f}")
