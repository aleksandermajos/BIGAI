from ENGINE.ALOHAPP_LANG_CODES import give_me_lang_code
import ollama

def generate_text(page):

    current_prompt = 'You have a limited vocabulary consisting of the following words: ' + page.main_page.user.prompt_present + '.Use ONLY provided words.' + 'Answer always in ' + give_me_lang_code(
                         page.main_language) + ' language and use maximal 2 short sentences'


    if page.text_gen == 'groq':
        if page.welcome:
            chat_completion = page.client_groq.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": current_prompt},
                    {"role": "user", "content": page.context}
                ],
                model="llama3-70b-8192",
            )
            page.welcome = False
        else:
            chat_completion = page.client_groq.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": current_prompt},
                    {"role": "user", "content": page.context}
                ],
                model="llama3-70b-8192",
            )
        bot_reply = chat_completion.choices[0].message.content

    if page.text_gen == 'ollama':
        bot_reply = ollama.chat(model='llama3.1:8b', messages=[
            {"role": "system",
             "content": current_prompt},
            {"role": "user", "content": page.context}
        ])
        bot_reply = bot_reply['message']['content']

    if page.text_gen == 'openai':
        response = page.client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": current_prompt},
                {"role": "user", "content": page.context}
            ]
        )
        bot_reply = response.choices[0].message.content

    return bot_reply