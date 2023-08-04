from llama_cpp import Llama
llm = Llama(model_path="ggml-vicuna-13b-4bit-rev1.bin")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)