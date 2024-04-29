from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path = path+'Mixtral-8x22B-v0.1-Q4_K_M.gguf'


llm = Llama(model_path=model_path,n_gpu_layers=78)
output = llm("Q: Write in 100 sentences best things to do in life... A: ", max_tokens=320, stop=["Q:", "\n"], echo=True)
print(output)