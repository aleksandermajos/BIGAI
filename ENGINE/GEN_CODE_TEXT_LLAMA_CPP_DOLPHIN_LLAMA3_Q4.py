from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path1 = path+'dolphin-2.9-llama3-8b.Q4_K_M.gguf'
llm1 = Llama(model_path=model_path1)

output = llm1("Q: Write in 10 sentences best things to do in life.... A: ", max_tokens=2000, stop=["Q:", "\n"], echo=True)
print(output)

