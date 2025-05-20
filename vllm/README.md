

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

### 🧪 Load Testing (WIP)

Use a load testing tool like [Locust](https://locust.io/), [wrk](https://github.com/wg/wrk), or custom Python scripts to simulate concurrent requests. Track:

* Mean latency
* Time-to-first-token (TTFT)
* Total tokens/sec under concurrency
* GPU KV cache usage

Results to be documented soon.

---

## 📁 Files

| File             | Description                                                       |
| ---------------- | ----------------------------------------------------------------- |
| `vllm_single.py` | Benchmark script for single request via `vllm` API                |
| `hf_single.py`   | Benchmark script for single request via Hugging Face Transformers |
| `load_test/`     | (WIP) Scripts for simulating concurrent users                     |
| `results/`       | Logs and structured benchmark results                             |

---

## 📊 Results Summary (so far)

| Approach        | TTFT (sec) | Tokens/sec | Notes                                             |
| --------------- | ---------- | ---------- | ------------------------------------------------- |
| vLLM (single)   | 1.51       | 56.77      | Overhead from engine init, optimized for batching |
| HF Transformers | 0.76       | 108.17     | Faster for isolated requests                      |
| vLLM (serve)    | TBD        | TBD        | Expected gains with concurrent users              |
| HF TGI          | TBD        | TBD        | Lightweight + performant                          |

---

## ✅ Goals

* [x] Set up vLLM and HF pipelines
* [x] Compare single-request latency
* [ ] Simulate and benchmark concurrent users
* [ ] Track GPU memory and token throughput
* [ ] Explore speculative decoding (future work)

---

## 🧠 Insights (preliminary)

* **vLLM** is well-suited for concurrent and batched inference scenarios.
* **HF** is lightweight for simple, single-turn use cases but may not scale as efficiently for multi-user inference.

---

## 📜 License

MIT License

---
