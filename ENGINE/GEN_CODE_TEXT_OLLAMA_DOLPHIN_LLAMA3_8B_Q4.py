import ollama
response = ollama.chat(model='dolphin-llama3', messages=[
  {
    'role': 'user',
    'content': 'Czy znasz jezyk polski?',
  },
])
print(response['message']['content'])