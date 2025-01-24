from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# Download the model
model_path = hf_hub_download(repo_id="city96/FLUX.1-dev-gguf", filename="flux-1b-Q4_K_M.gguf")

llm = Llama(model_path=model_path)
# Generate text
output = llm("Your input prompt here", max_tokens=50)
print(output['choices'][0]['text'])