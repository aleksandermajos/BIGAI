import ollama
from ENGINE.ALOHAPP_MAIL import send_mail
from pydantic import BaseModel


class TranslationResponseOllama(BaseModel):
    japanese: str
    english: str


def generate_text(page, user_text):
    system_prompt = (
        f'You are a super helpful language teacher. You are teaching {page.main_language}. '
        f'User is trying to learn {page.main_language}. '
        f'User knows the following words: {page.main_page.user.prompt_present}. '
        'Use as many of these words as possible, but you may include small grammar words that are needed to form a correct sentence. '
        'You have to produce at least one sentence in the target language. Be cheerful and funny. '
        'Arrange your answers in such a way as to encourage the user to continue the discussion. '
        'Be informative and answer the question. '
        "IMPORTANT: Return your entire answer as a JSON object in the format:"
        '{"japanese": "<Japanese response>", "english": "<English translation>"}'
    )
    #info_send =  send_mail(body=system_prompt)
    last_conversation = page.context
    mess = []
    lines = last_conversation.split('.')
    for line in lines:
        if line.startswith("user:"):
            mess.append({"role": "user", "content": line.replace("user:", "").strip()})
        elif line.startswith("assistant:"):
            mess.append({"role": "assistant", "content": line.replace("assistant:", "").strip()})




    if page.text_gen == 'groq':
        if page.welcome or not last_conversation.strip():
            messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
            chat_completion = page.client_groq.chat.completions.create(
                messages=messages,
                response_format={"type": "json_object"},
                model="llama3-70b-8192",
            )
            page.welcome = False
        else:
            messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
            chat_completion = page.client_groq.chat.completions.create(
                messages=messages,
                response_format={"type": "json_object"},
                model="llama3-70b-8192",
            )
        bot_reply = chat_completion.choices[0].message.content

    if page.text_gen == 'cerebras':
        messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
        chat_completion = page.client_cerebras.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="llama-3.3-70b",
        )
        bot_reply = chat_completion.choices[0].message.content

    if page.text_gen == 'ollama':
        messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
        bot_reply = ollama.chat(
            model='llama3.1:8b',
            messages=messages,

        )
        bot_message = bot_reply['message']['content']
        bot_reply = TranslationResponseOllama.parse_raw(bot_message)

    if page.text_gen == 'openai':
        messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
        response = page.client_openai.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model = "gpt-4o"
        )
        bot_reply = response.choices[0].message.content

    return bot_reply