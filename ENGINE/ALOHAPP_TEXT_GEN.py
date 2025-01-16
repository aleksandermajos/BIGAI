from ENGINE.ALOHAPP_LANG_CODES import get_lang_name_to_tts_melo, get_lang_name_to_nllb
from ENGINE.API_BIGAI_CLIENT import translate, detect_language
import ollama

def generate_text(page, user_text):
    system_prompt = 'You are super helpful language teacher.User try to learn ' + page.main_language + '.' + 'User knows only following words: ' + page.main_page.user.prompt_present + '.Use only provided words.' + 'Answer always in ' + page.main_language + ' language and use maximal 2 short sentences.In any circumstances do not reply in other language that' + page.main_language+' of any part of reply'

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
                model="llama3-70b-8192",
            )
            page.welcome = False
        else:
            messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
            chat_completion = page.client_groq.chat.completions.create(
                messages=messages,
                model="llama3-70b-8192",
            )
        bot_reply = chat_completion.choices[0].message.content

    if page.text_gen == 'ollama':
        bot_reply = ollama.chat(model='llama3.1:8b', messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": last_conversation}
        ])
        bot_reply = bot_reply['message']['content']

    if page.text_gen == 'openai':
        response = page.client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": last_conversation}
            ]
        )
        bot_reply = response.choices[0].message.content

    return bot_reply