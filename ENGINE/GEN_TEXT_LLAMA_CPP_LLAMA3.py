from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path = path+'Meta-Llama-3-8B-Instruct-Q5_K_M.gguf'


llm = Llama(model_path=model_path)
output = llm("Q: Name the planets in the solar system in Spanish language? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)