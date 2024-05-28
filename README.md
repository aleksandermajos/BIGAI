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

### BIGAI_SCHOOL:
| NAME                                                      | ENGINE USE                                                    | TIME   |
|-----------------------------------------------------------|---------------------------------------------------------------|--------|
| AUDIO TO SRT                                              | STT,TRANSLATE, FASTAPI                                        | 5      |
| AUDIO TO LECTOR                                           | STT,TTS , FASTAPI                                             | 4      |
| VOICE TO PIC                                              | SST,GEN PICTURE, FASTAPI                                      | 4      |
| PIC TO VOICE                                              | TTS, PIC RECOGNIZE, FASTAPI                                   | 3      |
| VOICE TO TRANSLATED VOICE                                 | STT, TTS, TRANSLATE,FASTAPI                                   | 3      |
| DIARY IN TARGET LANGUAGE                                  | STT, TTS, TRANSLATE,FASTAPI                                   | 3      |
| RADIO TO PIC                                              | STT, GEN PICTURE, FASTAPI                                     | 3      |
| OCR FROM PIC                                              | OCR ROMAN, OCR KANJI, FASTAPI                                 | 6      |
| UNSTRUCTURED DATA TO STRUCTURED DATA                      | PANDAS, FASTAPI                                               | 6      |
| FLASHCARDS WORDS, SENTENCES TO VOICE                      | TTS, ANKI, FASTAPI                                            | 6      |
| WORDS TO SENTENCES                                        | GEN CODE_TEXT , FASTAPI                                       | 4      |
| SENTENCES TO FLASHCARDS                                   | PANDAS, ANKI, SPACY, FASTAPI                                  | 6      |
| CUSTOM FLASHCARDS FROM WORDS,SENTENCES,PICTURES,RADIO     | STT,TTS, ANKI, PANDAS,TRANSLATE,SPACY, FASTAPI                | 6      |
| CONVERSATIONS AI WITH PICS AND MODULAR WORDS SELECTION    | TTS,STT, GEN PICTURE, TRANSLATE, FASTAPI                      | 6      |
| NETFLIX RECOMMENDATIONS                                   | PANDAS                                                        | 4      |
| RADIO/PODCAST RECOMMENDATIONS                             | PANDAS                                                        | 4      |
| MUSIC RECOMMENDATIONS                                     | PANDAS                                                        | 4      |
| BOOK RECOMMENDATIONS                                      | PANDAS                                                        | 5      |
| VOICE TO COMIC                                            | STT, GEN PICTURE, FASTAPI                                     | 4      |
| COMIC TO VOICE                                            | PIC RECOGNIZER, TTS, FASTAPI                                  | 4      |
| INSIGHTS FROM DATA                                        | PANDAS, SEABORN , FASTAPI                                     | 6      |
| CREATE SETTINGS                                           | PANDAS, SEABORN , FASTAPI                                     | 6      |
| DRAW KANJI WITH SENTENCES AND AUDIO                       | OCR KANJI, TTS, SPACY, FASTAPI                                | 6      |
| WELCOME WINDOW                                            | OCR KANJI, TTS, SPACY, FASTAPI                                | 10     |
| CONVERSATIONS HUMAN WITH PICS AND MODULAR WORDS SELECTION | TTS,STT, GEN PICTURE, TRANSLATE, FASTAPI                      | 12     |
| ANDROID FLET                                              | FLET, ANDROID                                                 | 12     |
| iOS FLET                                                  | FLET, ANDROID                                                 | 12     |
| WEB FLET                                                  | FLET, ANDROID                                                 | 8      |
| --------------------------------------------------------  | ------------------------------------------------------------- | ------ |
| SUMMA                                                     |                                                               | 161    |
| --------------------------------------------------------  | ------------------------------------------------------------- | ------ |
| AGENTIC, GEN CODE x 36 (BIGAI_ENGINE)(BIGAI_SCHOOL)       | GEN CODE_TEXT, GEN CREW, FINE TUNED, RAG, GEN GRAPH           | 90     |
| TIMESERIES RELATED CODE x 24 (QM)                         | GEN TIMELINE, GEN TIMESERIES, RECOGNIZE TIMELINE/TIMESERIES   | 60     |
| MARKETING LLM x 12 (BIGAI_MARKETING)                      | GEN TIMELINE, GEN TIMESERIES, RECOGNIZE TIMELINE/TIMESERIES   | 30     |
| FINANCE GET LLM x 12 (BIGAI_FINANCE)                      | GEN TIMELINE, GEN TIMESERIES, RECOGNIZE TIMELINE/TIMESERIES   | 30     |
| UNREAL 5 FRONTEND x24 (BIGAI_FRONT)                       | USING REALTIME INJECTIONS OF ANY OF AI                        | 100    |
| SAMURAI GROUP x80 (SAMURAI)                               | SAMURAI BASED APPS                                            | 200    |
| BIGAI_BUSINESS x50 (BIGAI_BUSINESS)                       | PRO BIGAI BUSINESS WITH INFRASTRUCTURE                        | 120    |
| ALOHA GROUP x50 (ALOHA)                                   | ALOHA GROUP BUSINESSES                                        | 120    |
| QUANT GROUP x50 (QUANT)                                   | QUANT GROUP BUSINESSES                                        | 120    |
| MOJO/RUST/C++ x25 (QUANT)                                 | PROGRAMMING LANGUAGES DIFF THAN PYTHON                        | 80     |
| --------------------------------------------------------  | ------------------------------------------------------------- | ------ |
| SUMMA                                                     |                                                               | 1040   |

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
| SAMURAI GROUP   | SAMURAI BASED APPS                                                     |
| BIGAI_BUSINESS  | TRACE YOUR BUSINESS ON A TIMELINE, AND BUILD NEW ONE                   |
| ALOHA GROUP     | ALOHA BASED APPS                                                       |
| QUANT GROUP     | QUANT BASED APPS                                                       |
| --------------- | ---------------------------------------------------------------------- |



### ENGINE NODES:
| NAME                                                     | EXTERNAL API   | IN BIGAI PROJECT        | MEMORY   |
|----------------------------------------------------------|----------------|-------------------------|----------|
| FASTAPI SERVER TRY                                       |                | EVERY                   | 0        |
| TTS                                                      | OPENAI API     |                         | 0        |
| STT                                                      |                |                         | 3        |
| TRANSLATE                                                |                |                         | 3        |
| GEN PICTURE                                              |                |                         | 12       |
| RECOGNIZE PICTURE                                        | CLOUDE HAIKU   |                         | 8        |
| OCR ROMAN, OCR KANJI                                     |                |                         | 6        |
| GEN COMIC                                                |                |                         | 16       |
| GEN VIDEO                                                |                |                         | 24       |
| GEN 3D OBJECTS                                           |                |                         | 24       |
| GEN VOICE/CLONE VOICE                                    |                |                         | 20       |
| GEN MUSIC                                                |                |                         | 18       |
| GEN TIMELINE                                             |                |                         | 6        |
| GEN TIMESERIES                                           |                |                         | 12       |
| RECOGNIZE TIMELINE/TIMESERIES                            |                |                         | 8        |
| RL AGENT                                                 |                |                         | 6*4=24   |
| GEN CODE_TEXT                                            | CLOUDE HAIKU   |                         | 3*24=76  |
| GEN CREW TOGETHER                                        |                |                         | 8        |
| GEN AUTOGEN TOGETHER                                     |                |                         | 8        |
| GEN LANGCHAIN TOGETHER                                   |                |                         | 8        |
| GEN LANGGRAPH TOGETHER                                   |                |                         | 12       |
| GEN DATA 5K TO CODE TASKS                                |                |                         | 0        |
| FINE TUNE CREW ON READY DATA                             |                |                         | 12       |
| FINE TUNE CREW ON DATA TO CODE                           |                |                         | 12       |
| RAG CREW ON READY DATA                                   |                |                         | 12       |
| RAG CREW ON DATA TO CODE                                 |                |                         | 12       |
| TEST CODE CREW                                           |                |                         | 0        |
| TRAIN OWN CREW ON FLET CODE FROM DOCUMENTATION USING RAG |                |                         | 18       |
| TRAIN OWN CREW ON TF CODE FROM DOCUMENTATION USING RAG   |                |                         | 18       |
| KNOWLEDGE OUTSIDE BOOK NLP                               |                |                         | 0        |
| GEN GRAPH KNOWLEDGE                                      |                |                         | 6        |
| GEN GRAPH REASONING                                      |                |                         | 12       |
| VISUALIZE SOLUTION ON GRAPH                              |                |                         | 0        |
| TRAIN OWN CREW ON ACTON AND API                          |                |                         | 18       |
| GEN GRAPH ACTION                                         |                |                         | 0        |
| TRAIN OWN CREW ON GRAPH ACTIONS                          |                |                         | 18       |
| FINDING EMPTY SPACES IN GRAPHS                           |                |                         | 6        |
| GENERATE CODE. KNOWLEDGE, REASONING OR ACTION IN GRAPHS  |                |                         | 18       |
| GENERATE FLET GUI FOR BIGAI_SCHOOL                       |                |                         | 12       |
| KNOWLEDGE OUTSIDE BOOK GRPAHS                            |                |                         | 12       |
| GEN INFRASTRUCTURE                                       |                |                         | 8        |
| GEN iOT ACTION                                           |                |                         | 0        |
| GEN EXTENSION WEB                                        |                |                         | 0        |
| -------------------------------------------------------  | -------------- | ----------------------- | -------- |




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




