import asyncio
import httpx
import time
import socket

NUM_REQUESTS = 40
PROMPT = "Describe how AI is transforming healthcare."
MAX_TOKENS = 100

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

async def wait_for_server(port, name):
    print(f"Waiting for {name} server...", end="")
    for _ in range(30):
        if is_port_open(port):
            print(" ready ✅")
            return
        print(".", end="", flush=True)
        await asyncio.sleep(1)
    raise RuntimeError(f"{name} server failed to start.")

async def send_request(client, url, payload, is_vllm, request_id, framework):
    start = time.time()
    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"\n❌ [{framework} #{request_id}] Request failed: {e}")
        print("Response text:", getattr(response, "text", "N/A"))
        return 0, 0

    # Extract prompt and text
    if is_vllm:
        prompt = payload["prompt"]
        text = data["choices"][0]["text"]
    else:
        prompt = payload["inputs"]
        text = data["generated_text"]

    end = time.time()

    # 🧾 Print full request and response
    print(f"\n[{framework} #{request_id}]")
    print(f"Prompt: {repr(prompt)}")
    print(f"Response: {repr(text)}")

    return end - start, len(text.split())

async def benchmark(api_name, url, payload, is_vllm):
    await wait_for_server(8000 if is_vllm else 8080, api_name)
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = [
            send_request(client, url, payload.copy(), is_vllm, i + 1, api_name.upper())
            for i in range(NUM_REQUESTS)
        ]
        start = time.time()
        results = await asyncio.gather(*tasks)
        end = time.time()

    latencies, token_counts = zip(*results)
    total_tokens = sum(token_counts)

    print(f"\n=== {api_name.upper()} Benchmark ===")
    print(f"Avg Latency: {sum(latencies)/NUM_REQUESTS:.4f} sec")
    print(f"Total Time: {end - start:.4f} sec")
    print(f"Tokens/sec: {total_tokens / (end - start):.2f}")

async def main():
    await benchmark(
        "vllm",
        "http://localhost:8000/v1/completions",
        {
            "model": "facebook/opt-125m",
            "prompt": PROMPT,
            "max_tokens": MAX_TOKENS
        },
        is_vllm=True
    )

    await benchmark(
        "hf",
        "http://localhost:8080/generate",
        {
            "inputs": PROMPT,
            "parameters": {
                "max_new_tokens": MAX_TOKENS,
                "temperature": 0.7,
                "do_sample": True
            }
        },
        is_vllm=False
    )

if __name__ == "__main__":
    asyncio.run(main())
