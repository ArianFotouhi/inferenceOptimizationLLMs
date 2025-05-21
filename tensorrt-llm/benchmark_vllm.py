import asyncio
import httpx
import time
import socket
import random

URL = "http://localhost:5000/v1/completions"
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_TOKENS = 80

# Prompts for completion-style model
TEST_PROMPTS = [
    "San Francisco is a",
    "Artificial intelligence can be defined as",
    "The theory of relativity explains that",
    "A healthy diet consists of",
    "During World War II,",
    "Photosynthesis is the process where",
    "The future of technology includes",
    "A cat typically spends its day",
    "The Amazon rainforest is known for",
    "A successful entrepreneur is someone who"
]

def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

async def wait_for_server(url, name="LLM"):
    host = url.split("//")[1].split("/")[0].split(":")[0]
    port = int(url.split(":")[-1].split("/")[0])
    print(f"Waiting for {name} server on {host}:{port}...", end="")
    for _ in range(30):
        if is_port_open(host, port):
            print(" ready ✅")
            return
        print(".", end="", flush=True)
        await asyncio.sleep(1)
    raise RuntimeError(f"{name} server at {url} failed to respond.")

async def send_completion_request(client, url, request_id):
    prompt = random.choice(TEST_PROMPTS)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7
    }

    start = time.time()
    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["text"]
    except Exception as e:
        print(f"\n❌ [Request #{request_id}] Failed: {e}")
        print("Response:", getattr(response, "text", "N/A"))
        return 0, 0

    end = time.time()

    print(f"\n[Request #{request_id}]")
    print(f"Prompt: {prompt}")
    print(f"Response: {text.strip()}")

    return end - start, len(text.split())

async def benchmark_concurrency(url, concurrency_level):
    await wait_for_server(url)
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = [
            send_completion_request(client, url, i + 1)
            for i in range(concurrency_level)
        ]
        print(f"\n🚀 Running benchmark with {concurrency_level} concurrent requests...")
        start = time.time()
        results = await asyncio.gather(*tasks)
        end = time.time()

    latencies, token_counts = zip(*results)
    total_tokens = sum(token_counts)
    successful_requests = sum(1 for l in latencies if l > 0)

    print(f"\n=== Benchmark @ {concurrency_level} Users ===")
    print(f"Successful Requests: {successful_requests}/{concurrency_level}")
    print(f"Avg Latency: {sum(latencies)/successful_requests:.4f} sec")
    print(f"Total Time: {end - start:.4f} sec")
    print(f"Tokens/sec: {total_tokens / (end - start):.2f}")

async def main():
    concurrency_levels = [20, 50, 80]  # Adjust as needed
    for level in concurrency_levels:
        await benchmark_concurrency(URL, level)

if __name__ == "__main__":
    asyncio.run(main())
