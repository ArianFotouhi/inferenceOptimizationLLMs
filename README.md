# LLM Inference Optimization Benchmarks
This repository explores the performance optimization of large language model (LLM) inference by comparing three prominent approaches:

### vLLM
An inference engine optimized for high throughput and low latency, leveraging techniques like continuous batching, paged attention, and FlashAttention.

### TensorRT-LLM
NVIDIA’s high-performance inference library designed for LLMs. It uses TensorRT and CUDA for aggressive graph optimization, kernel fusion, and GPU utilization to accelerate model execution, especially on NVIDIA hardware.

### Hugging Face Transformers
The standard approach for serving models using the transformers library, often paired with Hugging Face's Text Generation Inference (TGI) server for production deployment.


## 🔍 Objective
Benchmark and analyze the performance of both vLLM and Hugging Face-based serving pipelines on:

Single request latency

Throughput under concurrent loads

## 📦 Environment
Models:
```
TinyLlama/TinyLlama-1.1B-Chat-v1.0
facebook/opt-125m
```
Hardware:
```
GPU-enabled (e.g., RTX 3060)
```
