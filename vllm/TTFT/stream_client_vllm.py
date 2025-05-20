import requests
import json

API_URL = "http://localhost:8000/v1/completions"

headers = {
    "Content-Type": "application/json",
}

payload = {
    "model": "facebook/opt-125m",
    "prompt": "Explain gravity in simple terms:\n",
    "max_tokens": 100,
    "temperature": 0.7,
    "stream": True
}

response = requests.post(API_URL, headers=headers, json=payload, stream=True)

for line in response.iter_lines():
    if line:
        if line.startswith(b"data: "):
            line_content = line[len(b"data: "):].decode("utf-8")
            if line_content.strip() == "[DONE]":
                break  # end of stream
            try:
                data = json.loads(line_content)
                print(data["choices"][0]["text"], end="", flush=True)
            except json.JSONDecodeError:
                print("\n[Warning] Received non-JSON data:", line_content)
