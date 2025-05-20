

## 📈 Benchmark 1: Single Request

### 🔧 Setup

#### vLLM

```bash
# Run the benchmark script
python3 vllm_single.py
```

**Sample Output**:

```
=== vLLM Single Request Benchmark ===
TTFT: 1.5149 sec
Total Latency: 1.5149 sec
Tokens Generated: 86
Tokens/sec: 56.77
```

#### Hugging Face (Transformers)

```bash
# Run the benchmark script
python3 hf_single.py
```

**Sample Output**:

```
=== HF Single Request Benchmark ===
TTFT: 0.7579 sec
Total Latency: 0.7581 sec
Tokens Generated: 82
Tokens/sec: 108.17
```

📌 *Observation*: HF's raw generation with `generate()` is faster for a single request, especially for small models, due to lower startup overhead.

---

## ⚙️ Benchmark 2: Concurrent Serving

### 🧪 Setup

#### vLLM Server

Start the vLLM server:

```bash
vllm serve facebook/opt-125m
```

The server is launched at `http://localhost:8000` with multiple available endpoints such as `/v1/completions`.

#### Hugging Face Text Generation Inference (TGI)

```bash
docker pull ghcr.io/huggingface/text-generation-inference:latest

docker run --gpus all --shm-size 1g -p 8080:80 \
  -v $HOME/.cache/huggingface:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id facebook/opt-125m \
  --port 80
```

Server runs on `http://localhost:8080`.

### ▶️ Run Benchmark

```bash
python3 benchmarks.py
Edit NUM_REQUESTS in the script to control concurrency level (e.g., 20, 40, etc.)
```

### 🧪 Load Testing (WIP)

Use a load testing tool like [Locust](https://locust.io/), [wrk](https://github.com/wg/wrk), or custom Python scripts to simulate concurrent requests. Track:

* Mean latency
* Time-to-first-token (TTFT)
* Total tokens/sec under concurrency
* GPU KV cache usage

Results to be documented soon.

---

The benchmark client is an async Python script using `httpx` and `asyncio` to simulate concurrent users.

---

## 📊 Benchmark Results

### ✅ 20 Concurrent Users

| Framework | Total Time (sec) | Tokens/sec |
|-----------|-------------------|-------------|
| vLLM      | 0.6712            | 1986.03     |
| HF TGI    | 1.5441            | 838.67     |

> ⚠️ HF TGI initially returned empty outputs due to misconfigured payload (missing `"inputs"` key). This was later fixed in the 40-user test.

---

### ✅ 40 Concurrent Users

| Framework | Total Time (sec) | Tokens/sec |
|-----------|-------------------|-------------|
| vLLM      | 0.6963            | 3606.27     |
| HF TGI    | 2.2310            |  1244.75    |

---

## 📈 Observations

- **vLLM** consistently delivers **much lower latency and higher throughput**, thanks to:
  - PagedAttention and token scheduling
  - Efficient batching under concurrency

- **HF TGI** is:
  - More stable for general-purpose use
  - But shows higher latency under load
  - Returned empty completions until the correct input format was used:
    ```json
    {
      "inputs": "...",
      "parameters": {
        "max_new_tokens": 100,
        "temperature": 0.7,
        "do_sample": true
      }
    }
    ```

- **Output Quality**:
  - Both systems generate odd or nonsensical outputs at times — expected from small models like `opt-125m`
  - Tuning parameters like `temperature`, `top_p`, and `repetition_penalty` helps improve generation diversity

---




## 📜 License

MIT License

---
