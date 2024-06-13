from API_BIGAI_CLIENT import generate_image
from ENGINE.KEY_GROQ import provide_key
from groq import Groq

client = Groq(
    api_key=provide_key()
)

def Bot_reply():
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Generate detailed prompt for stable diffusion or midjourney.Answer only in prompt"},
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

for i in range(100):
    text = Bot_reply()
    print(text)
    generate_image(prompt=text,negative_prompt='',num_inference_steps=56,save_path="image"+str(i)+'.png')



oko=4