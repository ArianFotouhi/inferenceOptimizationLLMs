# LLM Inference Optimization Benchmarks
This repository explores the performance optimization of large language model (LLM) inference by comparing two prominent approaches:

vLLM: An inference engine optimized for throughput and low latency with advanced techniques like continuous batching and FlashAttention.

Hugging Face Transformers: The standard approach for serving models via the transformers library and Hugging Face's Text Generation Inference server.

## 🔍 Objective
Benchmark and analyze the performance of both vLLM and Hugging Face-based serving pipelines on:

Single request latency

Throughput under concurrent loads

## 📦 Environment
Model:
```
facebook/opt-125m
```
Hardware:
```
GPU-enabled (e.g., RTX 3060)
```
