import anthropic
import os

client = anthropic.Anthropic(
    api_key= os.environ.get("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=2000,
    temperature=1,
    system="You are an expert in short and precise answers ",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Can You tell me why a sky is blue?"
                }
            ]
        }
    ]
)
print(message.content[0].text)
file = open("CODE_GEN_BY_CLOUDE_HAIKU.py", "w")
file.write(message.content[0].text)
file.close()
