from crewai.tools import tool
from crewai import Agent
from crewai import Task, Crew
import requests
from KEY_GROQ import provide_key
from groq import Groq
import os
from ENGINE.ALOHAPP_LANG_CODES import *
from pydantic import BaseModel, Field
from typing import Literal

groq_key = provide_key()
os.environ["GROQ_API_KEY"] =groq_key

from crewai.tools import tool
from crewai import Agent, Task, Crew
import requests
from KEY_GROQ import provide_key
import os
from ENGINE.ALOHAPP_LANG_CODES import *

# Set Groq API key
groq_key = provide_key()
os.environ["GROQ_API_KEY"] = groq_key




# Define valid language codes
VALID_LANGUAGE_CODES = {'pl', "jp", "ja", "en", "English", "es", "fr", "French","de","zh","ko"}

@tool('TranslationTool')
def translation_tool(text: str, source_language: str, target_language: str) -> str:
    """
    Translates text from a source language to a target language using the FastAPI translation service.
    """
    # Validate input language codes
    if source_language not in VALID_LANGUAGE_CODES:
        raise ValueError(f"Invalid source_language: {source_language}. Must be one of {VALID_LANGUAGE_CODES}.")
    if target_language not in VALID_LANGUAGE_CODES:
        raise ValueError(f"Invalid target_language: {target_language}. Must be one of {VALID_LANGUAGE_CODES}.")

    url = "http://127.0.0.1:8000/translate"
    source_language = get_lang_name_to_nllb(source_language)
    target_language = get_lang_name_to_nllb(target_language)
    print(f"Source Language (NLLB): {source_language}")
    print(f"Target Language (NLLB): {target_language}")

    payload = {
        "text": text,
        "source_language": source_language,
        "target_language": target_language
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        translated_text = response.json().get("translated_text")
        return translated_text
    else:
        raise Exception(f"Error: {response.status_code} - {response.json().get('detail')}")

# Define the translator agent
translator_agent = Agent(
    role='Translator',
    goal='Translate text from one language to another.',
    backstory="You are a highly skilled AI translator. You are provided text and source/target language information. Your primary task is to use the 'TranslationTool' to translate the text. **The text you need to translate is given in the task context.** Once you have the translated text, you MUST return ONLY the translated text using the `Final Answer:` format.",
    tools=[translation_tool],
    verbose=True,
    llm="groq/llama3-8b-8192",
    max_iterations=1
)

# Define the translation task
translation_task = Task(
    description="You will be given an input text, a source language, and a target language. You MUST use the provided source_language and target_language exactly as given. Do NOT guess or override them. Use the 'TranslationTool' to translate the given input text to the target language. After using the tool, your final output must only contain the translated text and should be in the format `Final Answer:` followed by the translated text.",
    expected_output='The translated text in the target language.',
    agent=translator_agent
)

# Create the crew
crew = Crew(
    agents=[translator_agent],
    tasks=[translation_task],
    verbose=True
)

# Input text and languages
input_text = 'Hello, how are You?'
source_language = "en"  # Use "eng" for English
target_language = "fr"  # Use "fra" for French

# Debugging: Print inputs
print(f"Input Text: {input_text}")
print(f"Source Language: {source_language}")
print(f"Target Language: {target_language}")

# Kickoff the crew
result = crew.kickoff(
    inputs={"text": input_text, "source_language": source_language, "target_language": target_language}
)

print(result)