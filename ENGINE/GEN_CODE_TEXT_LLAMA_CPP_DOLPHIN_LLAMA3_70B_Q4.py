from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path = path+'dolphin-2.9-llama3-70b.Q4_0.gguf'


llm = Llama(model_path=model_path,n_gpu_layers=78)
output = llm("Q: Write in 100 sentences best things to do in life... A: ", max_tokens=320, stop=["Q:", "\n"], echo=True)
print(output)