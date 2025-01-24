from openai import OpenAI
from KEY_DEEPSEEK import provide_key
key = provide_key()
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model='deepseek-reasoner',
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)