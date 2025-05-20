from huggingface_hub import InferenceClient

client = InferenceClient("http://localhost:8080")

response = client.text_generation(
    "What is gravity?",
    stream=True,
    max_new_tokens=50
)

for token in response:
    print(token, end="", flush=True)
