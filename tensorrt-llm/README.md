# 🔍 LLM Inference Performance Benchmark: vLLM vs TensorRT-LLM

The model used in both tests is:  
`TinyLlama/TinyLlama-1.1B-Chat-v1.0`

Benchmarks are conducted using a consistent prompt format, based on OpenAI's `chat/completions` API.

---

## 📂 Files

- `benchmark_vllm.py`: Benchmark script for vLLM
- `benchmark_tensorrtllm.py`: Benchmark script for TensorRT-LLM

---

## 🚀 How to Run

### Run vLLM benchmark:
```bash
python benchmark_vllm.py
````

### Run TensorRT-LLM benchmark:

```bash
python benchmark_tensorrtllm.py
```

Make sure each corresponding server is already running and listening on the correct port before starting the script.

---

## 📊 Results

| Concurrency | Backend      | Avg Latency (sec) | Total Time (sec) | Tokens/sec | Successful Requests |
| ----------- | ------------ | ----------------- | ---------------- | ---------- | ------------------- |
| 80          | vLLM         | 1.3634            | 1.5618           | 2547.06    | 80 / 80             |
| 80          | TensorRT-LLM | 1.5410            | 1.6711           | 2543.24    | 80 / 80             |
| 50          | vLLM         | 1.0532            | 1.1026           | 2388.85    | 50 / 50             |
| 50          | TensorRT-LLM | 1.0983            | 1.3442           | 1748.31    | 50 / 50             |
| 20          | vLLM         | 2.3210            | 2.3587           | 452.80     | 20 / 20             |
| 20          | TensorRT-LLM | 1.4477            | 1.5442           | 672.83     | 20 / 20             |

---

## 📝 Notes

* All tests use a consistent list of 10 diverse natural language prompts.
* Both servers were benchmarked using the same machine and same model version.
* `max_tokens` was set to 80 in all requests.

---

## 📌 Conclusion

At higher concurrency (80 users), both vLLM and TensorRT-LLM deliver similar throughput (~2540 tokens/sec), with vLLM slightly faster in latency.
vLLM outperforms TensorRT-LLM at lower concurrency (20 users) in both latency and token generation speed.
Overall, vLLM demonstrates more consistent scalability across different user loads.

---

## 🔧 Requirements

* Python 3.8+
* Dependencies: `httpx`, `asyncio`

Install them with:

```bash
pip install httpx
```


