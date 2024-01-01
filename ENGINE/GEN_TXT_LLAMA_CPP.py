from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path = path+'llama-2-7b.Q4_K_S.gguf'


llm = Llama(model_path=model_path)
output = llm("Q: Name the planets in the solar system in Spanish language? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)