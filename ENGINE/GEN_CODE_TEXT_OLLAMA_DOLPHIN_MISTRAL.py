import ollama
response = ollama.chat(model='dolphin-mixtral', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])