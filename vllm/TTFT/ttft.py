import time
import asyncio
import aiohttp
import statistics
import uuid
from typing import List

NUM_REQUESTS = 60
PROMPT = "What is gravity?"
MAX_NEW_TOKENS = 50

VLLM_URL = "http://localhost:8000/v1/completions"
HF_URL = "http://localhost:8080/generate_stream"

HEADERS = {"Content-Type": "application/json"}

async def measure_ttft(session, url, payload, label, request_id: str) -> float:
    print(f"\n[{label} - {request_id}] Prompt: {payload.get('prompt') or payload.get('inputs')}")
    start = time.perf_counter()
    async with session.post(url, json=payload) as resp:
        async for line in resp.content:
            if line:
                ttft = time.perf_counter() - start
                try:
                    line_str = line.decode("utf-8")
                except Exception:
                    line_str = str(line)
                print(f"[{label} - {request_id}] First response: {line_str.strip()[:100]}")
                print(f"[{label} - {request_id}] TTFT: {ttft:.3f} sec")
                return ttft
    return -1.0

async def run_benchmark(api_name: str, url: str, payload_builder):
    print(f"\n🚀 Testing {api_name} with {NUM_REQUESTS} concurrent requests...")
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [
            asyncio.create_task(measure_ttft(session, url, payload_builder(), api_name, f"req-{i+1}"))
            for i in range(NUM_REQUESTS)
        ]
        ttfts = await asyncio.gather(*tasks)
        valid_ttfts = [t for t in ttfts if t > 0]
        avg_ttft = statistics.mean(valid_ttfts) if valid_ttfts else -1
        print(f"\n✅ {api_name} Average TTFT: {avg_ttft:.3f} sec over {len(valid_ttfts)} requests\n")

def build_payload_vllm():
    return {
        "model": "facebook/opt-125m",
        "prompt": PROMPT,
        "max_tokens": MAX_NEW_TOKENS,
        "stream": True
    }

def build_payload_hf():
    return {
        "inputs": PROMPT,
        "parameters": {"max_new_tokens": MAX_NEW_TOKENS},
        "stream": True
    }

if __name__ == "__main__":
    asyncio.run(run_benchmark("vLLM", VLLM_URL, build_payload_vllm))
    asyncio.run(run_benchmark("HuggingFace TGI", HF_URL, build_payload_hf))
