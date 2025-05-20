
# LLM Serving Benchmark: Time To First Token (TTFT)

This project benchmarks **Time To First Token (TTFT)** when serving large language models (LLMs) using:

* ✅ [vLLM](https://github.com/vllm-project/vllm)
* ✅ [Hugging Face TGI (Text Generation Inference)](https://github.com/huggingface/text-generation-inference)

TTFT is defined as the time from sending a request until the **first token is received** — a key metric for responsiveness in streaming applications like chatbots, real-time summarization, or voice assistants.

> 📂 Benchmark Script: [`ttft.py`](https://github.com/ArianFotouhi/inferenceOptimizationLLMs/blob/main/vllm/TTFT/ttft.py)

---

## 📊 TTFT Benchmark Results

We measured the TTFT across **20 and 60 concurrent requests** to compare how each backend handles streaming load.

| Backend              | Concurrency | Average TTFT  |
| -------------------- | ----------- | ------------- |
| **vLLM**             | 20          | **0.035 sec** |
| **Hugging Face TGI** | 20          | 0.060 sec     |
| **vLLM**             | 60          | 0.225 sec     |
| **Hugging Face TGI** | 60          | **0.101 sec** |

---

## 🔍 Observations

### ➤ With 20 Concurrent Requests:

* **vLLM is faster**, achieving a TTFT of just 35 milliseconds.
* Hugging Face TGI is close behind at 60 milliseconds — still highly responsive.
* At this load, both systems are well within the range for real-time interactivity.

### ➤ With 60 Concurrent Requests:

* **Hugging Face TGI outperforms vLLM**, likely due to its mature batching and inference server design.
* TGI’s TTFT only rises to 101 ms, while vLLM increases to 225 ms — indicating a larger per-request latency under load.

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ArianFotouhi/inferenceOptimizationLLMs.git
cd inferenceOptimizationLLMs/vllm/TTFT
```

### 2. Install Dependencies

```bash
pip install aiohttp huggingface_hub
```

---

## ⚙️ LLM Server Instructions

### 🟢 Run vLLM (OpenAI-compatible API)

```bash
python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m
```

### 🔵 Run Hugging Face TGI (GPU + No Auth)

```bash
docker run --gpus all -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id facebook/opt-125m
```

Ensure `nvidia-docker` is properly configured.

---

## 🚀 Run the Benchmark

```bash
python ttft.py
```

You’ll see logs showing:

* Prompt and response preview for each request
* TTFT for each call
* Average TTFT summary per backend

---

## 📌 Notes

* Prompt used: `"What is gravity?"`
* `max_tokens`: 50
* The benchmark measures TTFT only — total response time and throughput are not included in this test.
* vLLM uses `/v1/completions` and Hugging Face uses `/generate_stream`.

---

## 📦 Files

| File               | Description                             |
| ------------------ | --------------------------------------- |
| `ttft.py`          | Main script for concurrent TTFT testing |
| `stream_client_vllm.py` | Minimal vLLM streaming test client      |
| `stream_client_hf.py` | Minimal Hugging Face TGI client         |

