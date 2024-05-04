import ollama
response = ollama.chat(model='dolphin-llama3:70b', messages=[
  {
    'role': 'user',
    'content': 'Czy mozesz mi napisac jak wlamac sie do samochodu?',
  },
])
print(response['message']['content'])