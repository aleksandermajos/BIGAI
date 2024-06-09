import ollama
response = ollama.chat(model='llama3', messages=[
{"role": "system", "content": "You are super rude assistant.Use only vulgar words"},
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response['message']['content'])