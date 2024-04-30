from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path1 = path+'Phi-3-mini-4k-instruct-q4.gguf'
llm1 = Llama(model_path=model_path1,n_gpu_layers=81)

output = llm1("Q: Write in 10 sentences best things to do in life.... A: ", max_tokens=2000, stop=["Q:", "\n"], echo=True)
print(output)