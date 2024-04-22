from llama_cpp import Llama
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"MODELS/TEXT/"
model_path1 = path+'dolphin-2.9-llama3-8b.Q4_K_M.gguf'
model_path2 = path+'dolphin-2.9-llama3-8b.Q4_K_S.gguf'
model_path3 = path+'dolphin-2.9-llama3-8b.Q5_K_M.gguf'
model_path4 = path+'dolphin-2.9-llama3-8b.Q5_K_S.gguf'
model_path5 = path+'dolphin-2.9-llama3-8b.Q6_K.gguf'


llm1 = Llama(model_path=model_path1)
llm2 = Llama(model_path=model_path2)
llm3 = Llama(model_path=model_path3)
llm4 = Llama(model_path=model_path4)
llm5 = Llama(model_path=model_path5)
output = llm1("Q: Na początku było tak, że bociana dziobał szpak, a później była zmiana i szpak dziobał bociana, a później były trzy takie zmiany, ile razy szpak był dziobany ? A: ", max_tokens=144, stop=["Q:", "\n"], echo=True)
print(output)
output = llm2("Q: Na początku było tak, że bociana dziobał szpak, a później była zmiana i szpak dziobał bociana, a później były trzy takie zmiany, ile razy szpak był dziobany ? A: ", max_tokens=144, stop=["Q:", "\n"], echo=True)
print(output)
output = llm3("Q: Na początku było tak, że bociana dziobał szpak, a później była zmiana i szpak dziobał bociana, a później były trzy takie zmiany, ile razy szpak był dziobany ? A: ", max_tokens=144, stop=["Q:", "\n"], echo=True)
print(output)
output = llm4("Q: Na początku było tak, że bociana dziobał szpak, a później była zmiana i szpak dziobał bociana, a później były trzy takie zmiany, ile razy szpak był dziobany ? A: ", max_tokens=144, stop=["Q:", "\n"], echo=True)
print(output)
output = llm5("Q: Na początku było tak, że bociana dziobał szpak, a później była zmiana i szpak dziobał bociana, a później były trzy takie zmiany, ile razy szpak był dziobany ? A: ", max_tokens=144, stop=["Q:", "\n"], echo=True)
print(output)
