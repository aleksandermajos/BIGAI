import ollama

res = ollama.chat(
	model="llava:13b",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': ['./images/1-1.png']
		}
	]
)

print(res['message']['content'])