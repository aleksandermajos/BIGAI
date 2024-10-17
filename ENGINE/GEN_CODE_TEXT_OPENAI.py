from ENGINE.KEY_OPENAI import provide_key
from openai import OpenAI


key=provide_key()
client = OpenAI(api_key=key)


def o1_preview():
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {
                "role": "user",
                "content": "Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4],[5,6]' and prints the transpose in the same format."
            }
        ]
    )

    print(response.choices[0].message.content)