# BIGAI
### MODULAR FRAMEWORK BASED ON MACHINE LEARNING AND DEEP LEARNING(LLM) ALGORITHMS FOR FAST PROTOTYPING

*⭐️ INSTALL REQUIREMENTS:*
pip install -r requirements_{your_operating_system}.txt

*⭐️ RECREATE CONDA ENVIROMENT:*
conda env create -f BIGAI_{your_operating_system}.yml

*⭐️ STARTING POINT:*
BIGAI/SCHOOL/NOTEBOOKS/ANY.ipynb
or
BIGAI/ENGINE/ANY.py

### MAIN MODULES:
* SCHOOL - PLAYGROUND FOR TESTING NEW CODE (USUALLY IN JUPYTER FORMAT) AND POSSIBLY CREATE NEW METHODS FOR ENGINE.
* ENGINE - TESTED METHODS FOR LATER USE BY PROJECTS
* FRONT - FRONTEND FOR PROJECTS.RECENTLY ALOHAPP AND QUANTMAVERICK
* MODELS - TRAINED MODELS AS WEIGHTS MOSTLY FOR PYTORCH
* DATA - DATA STORAGE FOR SMALL FILES

### SCHOOL PLAYGROUND:
| NAME                                                   | ENGINE USE                                                  |
|--------------------------------------------------------|-------------------------------------------------------------|
| AUDIO TO SRT                                           | STT,TRANSLATE, FASTAPI                                      |
| AUDIO TO LECTOR                                        | STT,TTS , FASTAPI                                           |
| VOICE TO PIC                                           | SST,GEN PICTURE, FASTAPI                                    |
| PIC TO VOICE                                           | TTS, PIC RECOGNIZE, FASTAPI                                 |
| VOICE TO VOICE                                         | STT, TTS, FASTAPI                                           |
| VOICE TO TRANSLATED VOICE                              | STT, TTS, TRANSLATE,FASTAPI                                 |
| DIARY IN TARGET LANGUAGE                               | STT, TTS, TRANSLATE,FASTAPI                                 |
| RADIO TO PIC                                           | STT, GEN PICTURE, FASTAPI                                   |
| OCR FROM PIC                                           | OCR ROMAN, OCR KANJI, FASTAPI                               |
| UNSTRUCTURED DATA TO STRUCTURED DATA                   | PANDAS, FASTAPI                                             |
| FLASHCARDS WORDS, SENTENCES TO VOICE                   | TTS, ANKI, FASTAPI                                          |
| WORDS TO SENTENCES                                     | GEN CODE_TEXT , FASTAPI                                     |
| SENTENCES TO FLASHCARDS                                | PANDAS, ANKI, SPACY, FASTAPI                                |
| CUSTOM FLASHCARDS FROM WORDS,SENTENCES,PICTURES,RADIO  | STT,TTS, ANKI, PANDAS,TRANSLATE,SPACY, FASTAPI              |
| CONVERSATIONS AI WITH PICS AND MODULAR WORDS SELECTION | TTS,STT, GEN PICTURE, TRANSLATE, FASTAPI                    |
| RECOMMEND SYSTEM ON NETFLIX                            | PANDAS                                                      |
| RECOMMEND SYSTEM ON MUSIC                              | PANDAS                                                      |
| RECOMMEND SYSTEM ON BOOK                               | PANDAS                                                      |
| VOICE TO COMIC                                         | STT, GEN PICTURE, FASTAPI                                   |
| COMIC TO VOICE                                         | PIC RECOGNIZER, TTS, FASTAPI                                |
| INSIGHTS FROM DATA                                     | PANDAS, SEABORN , FASTAPI                                   |
| CREATE SETTINGS                                        | PANDAS, SEABORN , FASTAPI                                   |
| DRAW KANJI WITH SENTENCES AND AUDIO                    | OCR KANJI, TTS, SPACY, FASTAPI                              |
| AGENTIC, GEN CODE x 36                                 | GEN CODE_TEXT, GEN CREW, FINE TUNED, RAG, GEN GRAPH         |
| TIMESERIES RELATED CODE x 8                            | GEN TIMELINE, GEN TIMESERIES, RECOGNIZE TIMELINE/TIMESERIES |
| RL RELATED CODE x 4                                    | GEN TIMELINE, GEN TIMESERIES, RECOGNIZE TIMELINE/TIMESERIES |






### ENGINE NODES:
| NAME                                                     | EXTERNAL API   | IN BIGAI PROJECT        | INTERNAL API   |
|----------------------------------------------------------|----------------|-------------------------|----------------|
| FASTAPI SERVER TRY                                       |                | ?                       |                |
| GEN CODE_TEXT                                            | CLOUDE HAIKU   |                         |                |
| GEN CREW TOGETHER                                        |                |                         |                |
| GEN AUTOGEN TOGETHER                                     |                |                         |                |
| GEN LANGCHAIN TOGETHER                                   |                |                         |                |
| GEN LANGGRAPH TOGETHER                                   |                |                         |                |
| GEN DATA 5K TO CODE TASKS                                |                |                         |                |
| FINE TUNE CREW ON READY DATA                             |                |                         |                |
| FINE TUNE CREW ON DATA TO CODE                           |                |                         |                |
| RAG CREW ON READY DATA                                   |                |                         |                |
| RAG CREW ON DATA TO CODE                                 |                |                         |                |
| TEST CODE CREW                                           |                |                         |                |
| TRAIN OWN CREW ON FLET CODE FROM DOCUMENTATION USING RAG |                |                         |                |
| TRAIN OWN CREW ON TF CODE FROM DOCUMENTATION USING RAG   |                |                         |                |
| KNOWLEDGE OUTSIDE BOOK NLP                               |                |                         |                |
| GEN GRAPH KNOWLEDGE                                      |                |                         |                |
| GEN GRAPH REASONING                                      |                |                         |                |
| VISUALIZE SOLUTION ON GRAPH                              |                |                         |                |
| TRAIN OWN CREW ON ACTON AND API                          |                |                         |                |
| GEN GRAPH ACTION                                         |                |                         |                |
| TRAIN OWN CREW ON GRAPH ACTIONS                          |                |                         |                |
| FINDING EMPTY SPACES IN GRAPHS                           |                |                         |                |
| GENERATE CODE. KNOWLEDGE, REASONING OR ACTION IN GRAPHS  |                |                         |                |
| GENERATE FLET GUI FOR BIGAI_SCHOOL                       |                |                         |                |
| KNOWLEDGE OUTSIDE BOOK GRPAHS                            |                |                         |                |
| TTS                                                      | OPENAI API     |                         |                |
| STT                                                      |                |                         |                |
| TRANSLATE                                                |                |                         |                |
| PROTOTYPE BIGAI_SCHOOL                                   |                |                         |                |
| GEN PICTURE                                              |                |                         |                |
| RECOGNIZE PICTURE                                        | CLOUDE HAIKU   |                         |                |
| OCR ROMAN, OCR KANJI                                     |                |                         |                |
| GEN COMIC                                                |                |                         |                |
| GEN VIDEO                                                |                |                         |                |
| GEN 3D OBJECTS                                           |                |                         |                |
| GEN VOICE/CLONE VOICE                                    |                |                         |                |
| GEN MUSIC                                                |                |                         |                |
| GEN TIMELINE                                             |                |                         |                |
| GEN TIMESERIES                                           |                |                         |                |
| RECOGNIZE TIMELINE/TIMESERIES                            |                |                         |                |
| RL AGENT                                                 |                |                         |                |
| GEN INFRASTRUCTURE                                       |                |                         |                |
| GEN iOT ACTION                                           |                |                         |                |
| GEN EXTENSION WEB                                        |                |                         |                |
| -------------------------------------------------------  | -------------- | ----------------------- | -------------- |



### BUSINESS BASED ON BIGAI:
| NAME            | PURPOSE                                                                |
|-----------------|------------------------------------------------------------------------|
| BIGAI_SCHOOL    | FOR LIGHT PROGRAMMING TASKS.VOICE TO CODE + INTERPRETER + AGENTS       |
| BIGAI_ENGINE    | CORE OF BIGAI.GRAPH BASED LLMs REASONING AND INTERPRETABILITY          |
| ALOHAPP         | MODULAR LEARNING LANGUAGE APP BASED ON COMPREHENSIBLE INPUT AND AGENTS |
| BIGAI_MARKETING | FOR A REASON TO BE VISIBLA SA YOUR BUSINESS                            |
| BIGAI_FINANCE   | FOR A REASON TO FIND SOURCES OF MONEY                                  |
| QUANTMAVERICK   | MODULAR "HEDGE FUND" AT HOME.TIME SERIES WITH POWER OF CREWAI AGENTS   |
| BIGAI_FRONT     | DIFFERENT FRONTENDS SIMILAR TO MODULAR NATURE OF LINUX                 |
| SAMURAIAPP      | TRACE YOUR HABITS ON A TIMELINE BASED ON AGENTS                        |
| BIGAI_BUSINESS  | TRACE YOUR BUSINESS ON A TIMELINE, AND BUILD NEW ONE                   |
| ALOHA GROUP     | ALOHA BASED APPS                                                       |
| QUANT GROUP     | QUANT BASED APPS                                                       |
| SAMURAI GROUP   | SAMURAI BASED APPS                                                     |
| --------------- | ---------------------------------------------------------------------- |


### THIS REPO IS SUPPLEMENT OF BIGAI YT CHANNEL:

https://www.youtube.com/channel/UCs5wP4tHR6vaWRWtpR4EKmA

*⭐️ Like this repo? please star & consider donating to keep it maintained*

<a href="https://www.buymeacoffee.com/aleksanderu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


### USE OF SPECIFIC FRAMEWORK/TOOL/WEBSITES IN BIGAI ENGINE:
* PYTORCH 2.2.2
* PYTORCH LIGHTNING
* PYTORCH GEOMETRIC
* TENSORFLOW 2.15.1
* JAX,TRAX
* PYCARET
* HUGGINGFACE
* LLAMA_CPP
* CREWAI
* AUTOGEN
* SWARMS
* SWE-AGENT
* LANGCHAIN
* LANGGRAPH
* LANGSMITH
* METAGPT
* DSPY
* WEIGHTS AND BIASES
* MLFLOW
* LM STUDIO
* GROQ PLAYGROUND
* FLET
* DOCKER
* KUBERNETES
* BIGAI API
* OPENAI API
* REKA API
* ANTHROPIC API
* GOOGLE GEMINI API
* ELEVENLABS API
* PLAYHT API
* EDENAI API
* TOGETHER.AI API
* XAI API
* GCP
* PYSPARK
* NEO4J




> **BEWARE**: This is a work in progress!
>
> * Code here may change and disappear without warning.
>
> * Major reorganizations may happen at any time.
>
> * No promises. No guarantees. Use at own risk.




