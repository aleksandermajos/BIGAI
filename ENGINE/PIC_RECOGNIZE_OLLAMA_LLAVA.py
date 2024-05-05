import ollama
from PIL import Image

res = ollama.chat(
	model="llava:13b",
	messages=[
		{
			'role': 'user',
			'content': 'Recognize text from this image:',
			'images': ['./images/ASSI.jpg']
		}
	]
)

print(res['message']['content'])