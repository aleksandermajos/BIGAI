from huggingface_hub import hf_hub_download
from llama_cpp import Llama


model_name = "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
model_file = "mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf"
model_path = hf_hub_download(model_name, filename=model_file)
llm = Llama(model_path=model_path, n_gpu_layers=60, n_ctx=3584, n_batch=521, verbose=True)

output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)
output = llm("Q: What is Your name? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)
output = llm("Q: What is purpose of live? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)