import ollama
from ENGINE.ALOHAPP_MAIL import send_mail
from pydantic import BaseModel
import json
import re
import asyncio


class TranslationResponseOllama(BaseModel):
    japanese: str
    english: str


def generate_text(page, user_text):
    if page.main_language == 'ja':
        index = page.main_page.user.langs.index(page.main_language)
        system_prompt = (
            f'You are a super helpful language teacher. You are teaching {page.main_language}. '
            f'User is trying to learn {page.main_language}. '
            f'User knows the following words: {page.main_page.user.prompt_present[index]}. '
            'Use some of these words if possible, but you may include small grammar words that are needed to form a correct sentence. '
            'You have to produce at least one average length  sentence in the target language. Be cheerful, funny and concise. '
            'Arrange your answers in such a way as to encourage the user to continue the discussion. '
            'Be informative and answer the question.Do not repeat yourself.Or do not repeat after me'
            "IMPORTANT: Return your entire answer as a JSON object in the format:"
            '{"japanese": "<Japanese response>", "english": "<English translation>"}'
        )
    if page.main_language == 'zh':
        index = page.main_page.user.langs.index(page.main_language)
        system_prompt = (
            f'You are a super helpful language teacher. You are teaching {page.main_language}. '
            f'User is trying to learn {page.main_language}. '
            f'User knows the following words: {page.main_page.user.prompt_present[index]}. '
            'Use some of these words if possible, but you may include small grammar words that are needed to form a correct sentence.'
            'You have to produce at least one average length  sentence in the target language. Be cheerful, funny and concise.'
            'Arrange your answers in such a way as to encourage the user to continue the discussion. '
            'Be informative and answer the question.Do not repeat yourself.Or do not repeat after me.'
            "IMPORTANT: Return your entire answer as a JSON object in the format:"
            '{"chinese": "<Chinese response>", "english": "<English translation>"}'
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

    if page.text_gen == 'openai':
        messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
        response = page.client_openai.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model = "gpt-4o"
        )
        bot_reply = response.choices[0].message.content

    if page.text_gen == 'google':

        messages = [{"role": "model", "parts": system_prompt},{"role": "user", "parts": user_text}]
        chat = page.google_model.start_chat(history=messages)
        response = chat.send_message(user_text)
        bot_reply = response.text



    if page.text_gen == 'cerebras':
        messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
        chat_completion = page.client_cerebras.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="llama-3.3-70b",
        )
        bot_reply = chat_completion.choices[0].message.content


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

    if page.text_gen == 'ollama':
        messages = [{"role": "system", "content": system_prompt}] + mess + [{"role": "user", "content": user_text}]
        bot_reply = ollama.chat(
            model='llama3.1:8b',
            messages=messages,

        )
        bot_message = bot_reply['message']['content']
        bot_reply = TranslationResponseOllama.parse_raw(bot_message)



    return bot_reply

def generate_sugestion(page, bot_text):
    if page.main_language == 'ja':
        index = page.main_page.user.langs.index(page.main_language)
        system_prompt = (
            f'You are a super helpful sentence analizer. You are analizing the sentence:  {bot_text}.'
            f'User is trying to learn {page.main_language}.'
            f'User knows the following words: {page.main_page.user.prompt_present[index]}.'
            f'You have to produce at least one small length sentence in a target language.The produced sentence is what you think is the best answer for {bot_text}.'
            'Use as many of these words , you may include small grammar words that are needed to form a correct sentence.'
            "IMPORTANT: Return your entire answer as a JSON object in the format:"
            '{"japanese": "<Japanese response>", "english": "<English translation>"}'
        )
    if page.main_language == 'zh':
        index = page.main_page.user.langs.index(page.main_language)
        system_prompt = (
            f'You are a super helpful sentence analizer. You are analizing the sentence:  {bot_text}.'
            f'User is trying to learn {page.main_language}. '
            f'User knows the following words: {page.main_page.user.prompt_present[index]}. '
            f'You have to produce at least one small length sentence in a target language.The produced sentence is what you think is the best answer for {bot_text}. '
            'Use as many of these words , you may include small grammar words that are needed to form a correct sentence. '
            "IMPORTANT: Return your entire answer as a JSON object in the format:"
            '{"chinese": "<Chinese response>", "english": "<English translation>"}'
        )

    if page.text_gen == 'openai':
        messages = [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": bot_text}]
        response = page.client_openai.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model = "gpt-4o"
        )
        bot_reply = response.choices[0].message.content

    if page.text_gen == 'cerebras':
        messages = [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": bot_text}]
        chat_completion = page.client_cerebras.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="llama-3.3-70b",
        )
        bot_reply = chat_completion.choices[0].message.content

    if page.text_gen == 'groq':
        messages = [{"role": "system", "content": system_prompt}]  + [{"role": "user", "content": bot_text}]
        chat_completion = page.client_groq.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="llama3-70b-8192",
        )
        bot_reply = chat_completion.choices[0].message.content

    return bot_reply

def generate_pos_tran(source,words,lang='ja',target_lang='en'):
    originals = ', '.join(word.original for word in words)

    system_prompt = (
        f'You are a super helpful words analyzer. You are analyzing the the words:  {originals}.'
        f'User is trying to learn {lang}.'
        f'Your task is for each word from list: {originals} create part_of_speech information and translation for each word into a {target_lang} language'
        "IMPORTANT: You MUST return your entire answer as a JSON object in the format every time:"
        '[words]'
        '{"original": "<word>", "part_of_speech": "<part_of_speech>", "translate": "<translate>"},'
        'Only one line like {"original": "<word>", "part_of_speech": "<part_of_speech>", "translate": "<translate>"} is NOT acceptable'
        'It need to contain all words'
    )

    if source.text_gen == 'openai':
        messages = [{"role": "system", "content": system_prompt}]
        response = source.client_openai.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="gpt-4o"
        )
        bot_reply = response.choices[0].message.content

    if source.text_gen == 'cerebras':
        messages = [{"role": "system", "content": system_prompt}]
        chat_completion = source.client_cerebras.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="llama-3.3-70b",
        )
        bot_reply = chat_completion.choices[0].message.content

    if source.text_gen == 'groq':
        messages = [{"role": "system", "content": system_prompt}]
        chat_completion = source.client_groq.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            model="llama3-70b-8192",
        )
        bot_reply = chat_completion.choices[0].message.content

    return bot_reply