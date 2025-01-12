from crewai.tools import tool
from crewai import Agent
from crewai import Task, Crew
import requests


@tool('TranslationTool')
def translation_tool(text: str, source_language: str, target_language: str) -> str:
    """
    Translates text from a source language to a target language using the FastAPI translation service.
    """
    url = "http://127.0.0.1:8000/translate"
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

translator_agent = Agent(
    role='Translator',
    goal='Translate text from one language to another.',
    backstory='An AI agent specialized in language translation tasks.',
    tools=[translation_tool],
    verbose=True
)

translation_task = Task(
    description='Translate the given text from one language to another',
    expected_output='Translated text in target language',
    agent= translator_agent
)

crew = Crew(
    agents=[translator_agent],
    tasks=[translation_task],
    verbose=True
)

input_text = 'Hello, how are You?'

crew.kickoff(inputs={'text': input_text, 'source_language': 'eng', 'target_language': 'fra'})

