from ENGINE.TTS_OPENAI import generate_and_play
from playsound import playsound
from fastapi import Form
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import platform
os_name = platform.system()


STT_WHISPERX = True
TTS_KOKORO = True
TTS_MELO = True
SPACY_STANZA = True
TRANSLATE_NLLB = True
LANG_DETECT_FT = True
GEN_IMAGE_SD3 = False

app = FastAPI()

if SPACY_STANZA:
    import os
    import spacy_stanza
    from typing import List

    if os_name == 'Darwin':

        lemma_pl = spacy_stanza.load_pipeline('pl')
        lemma_en = spacy_stanza.load_pipeline('en')
        lemma_ja = spacy_stanza.load_pipeline('ja')
        lemma_zh = spacy_stanza.load_pipeline('zh')
        '''
        lemma_fr = spacy_stanza.load_pipeline('fr')
        lemma_es = spacy_stanza.load_pipeline('es')
        lemma_it = spacy_stanza.load_pipeline('it')
        lemma_pt = spacy_stanza.load_pipeline('pt')
        '''

    if os_name == 'Linux':
        lemma_pl = spacy_stanza.load_pipeline('pl',device='cuda:0')
        lemma_en = spacy_stanza.load_pipeline('en',device='cuda:0')
        lemma_ja = spacy_stanza.load_pipeline('ja', device='cuda:0')
        lemma_zh = spacy_stanza.load_pipeline('zh', device='cuda:0')

        '''
        lemma_fr = spacy_stanza.load_pipeline('fr', device='cuda:0')
        lemma_es = spacy_stanza.load_pipeline('es',device='cuda:0')
        lemma_it = spacy_stanza.load_pipeline('it',device='cuda:0')
        lemma_pt = spacy_stanza.load_pipeline('pt', device='cuda:0')
        '''



    # Define request and response models
    class LemmatizeRequest(BaseModel):
        sentences: List[str]
        lang: str


    class LemmatizeResponse(BaseModel):
        lemmatized_sentences: List[List[str]]


    @app.post("/lemmatize", response_model=LemmatizeResponse)
    async def lemmatize(request: LemmatizeRequest):
        if not request.sentences:
            raise HTTPException(status_code=400, detail="No sentences provided.")
        lang = request.lang


        if lang == 'pl': lemma = lemma_pl
        if lang == 'en': lemma = lemma_en
        if lang == 'ja': lemma = lemma_ja
        if lang == 'zh': lemma = lemma_zh



        lemmatized_sentences = []
        for sentence in request.sentences:
            lem = lemma(sentence)
            lem_text = []
            for token in lem:
                lem_text.append(str(token.lemma_))
            unwanted_elements = [']','[','。', '?', '.', '_', ' ', ', ', ',','，']
            filtered_lem_text = [item for item in lem_text if item not in unwanted_elements]
            lemmatized_sentences.append(filtered_lem_text)


        return LemmatizeResponse(lemmatized_sentences=lemmatized_sentences)




if LANG_DETECT_FT:
    import os
    import fasttext

    if os_name == 'Darwin':
        MODEL_PATH = r'/Users/bigai/PycharmProjects/BIGAI/MODELS/TEXT/fasttext/lid.176.bin'

    if os_name == 'Linux':
        MODEL_PATH = r'/home/bigai/PycharmProjects/BIGAI/MODELS/TEXT/fasttext/lid.176.bin'

    # Check if the model file exists, if not, download it
    if not os.path.exists(MODEL_PATH):
        import urllib.request

        print("Downloading model...")
        url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'
        urllib.request.urlretrieve(url, MODEL_PATH)
        print("Model downloaded.")

    # Load the FastText language identification model
    model_FT  = fasttext.load_model(MODEL_PATH)


    class TextInput(BaseModel):
        text: str


    @app.post('/detect_language')
    async def detect_language(input: TextInput):
        # Use the FastText model to predict the language
        predictions = model_FT.predict(input.text, k=1)  # Get top prediction
        label = predictions[0][0]  # e.g., '__label__en'
        language_code = label.replace('__label__', '')  # e.g., 'en'
        confidence = predictions[1][0]  # e.g., 0.99

        return {'language_code': language_code, 'confidence': confidence}


if STT_WHISPERX:
    if os_name == 'Darwin':
        from lightning_whisper_mlx import LightningWhisperMLX
        import numpy as np
        import whisperx
        model = LightningWhisperMLX(model="large", batch_size=12, quant=None)


        @app.post("/transcribe/")
        async def transcribe(file: UploadFile = File(...), language: str = Form(...), file_path: str = Form(...)):
            audio = whisperx.load_audio(file_path)
            audio_np = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0
            if language == 'zz': text = model.transcribe(audio)['text']
            else: text = model.transcribe(audio,language=language)['text']

            return JSONResponse(content=text)


    if os_name == 'Linux':
        import whisperx
        model = whisperx.load_model("large-v3", device="cuda")


        @app.post("/transcribe/")
        async def transcribe(file: UploadFile = File(...), language: str = Form(...), file_path: str = Form(...)):
            print('before load audio')
            audio = whisperx.load_audio(file_path)
            print('after load audio')
            print('before transcribe')
            if language == 'zz': language=''
            result = model.transcribe(audio, batch_size=16, task="transcribe",language=language)
            print('after transcribe')
            if result is None:
                result = 'Transcribe error'
            make_source = False
            if make_source:
                print('before align transcribe')
                device = 'cuda:0'
                model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
                result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
                print('after align transcribe')


                response_data = {
                    "segments": result["segments"]
                }

            print('before return')
            print(JSONResponse(content=result))
            return JSONResponse(content=result)
if TTS_KOKORO:
    from playsound import playsound
    from fastapi.responses import FileResponse
    from ALOHAPP_LANG_CODES import get_lang_name_to_tts_kokoro, get_speaker_name_to_tts_kokoro
    from kokoro import KPipeline
    import soundfile as sf

    pipeline_en = KPipeline(lang_code='b')
    pipeline_fr = KPipeline(lang_code='f')
    pipeline_it = KPipeline(lang_code='i')
    pipeline_zh = KPipeline(lang_code='z')
    pipeline_ja = KPipeline(lang_code='j')
    pipeline_pt = KPipeline(lang_code='p')
    pipeline_es = KPipeline(lang_code='e')


    class TextRequest(BaseModel):
        text: str
        lang: str
        output_path: str


    @app.post("/tts_kokoro")
    async def tts_kokoro(request: TextRequest):
        text = request.text
        lang_beg = request.lang
        output_path = request.output_path

        if get_lang_name_to_tts_kokoro(lang_beg):

            lang = get_lang_name_to_tts_kokoro(lang_beg)
            if lang_beg == 'en': pipeline = pipeline_en
            if lang_beg == 'fr': pipeline = pipeline_fr
            if lang_beg == 'it': pipeline = pipeline_it
            if lang_beg == 'zh': pipeline = pipeline_zh
            if lang_beg == 'ja': pipeline = pipeline_ja
            if lang_beg == 'pt': pipeline = pipeline_pt
            if lang_beg == 'es': pipeline = pipeline_es

            speaker = get_speaker_name_to_tts_kokoro(lang_beg)
            generator = pipeline(
                text, voice=speaker,  # <= change voice here
                speed=0.75, split_pattern=r'\n+'
            )


        else:
            generate_and_play(text,'nova',path=output_path)
            lang = lang_beg



        if not text or not lang or not output_path:
            raise HTTPException(status_code=400, detail="text,lang,output_path is required")
        if get_lang_name_to_tts_kokoro(lang_beg):
            try:
                for i, (gs, ps, audio) in enumerate(generator):
                    print(i)  # i => index
                    print(gs)  # gs => graphemes/text
                    print(ps)  # ps => phonemes
                    sf.write(output_path, audio, 24000)
                    playsound(output_path)


                return FileResponse(output_path, media_type="audio/wav", filename=output_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))



if TTS_MELO:
    from melo.api import TTS
    from fastapi.responses import FileResponse
    from ALOHAPP_LANG_CODES import get_lang_name_to_tts_melo, get_speaker_name_to_tts_melo


    class TextRequest(BaseModel):
        text: str
        lang: str
        output_path: str


    @app.post("/tts_melo")
    async def tts_melo(request: TextRequest):
        text = request.text
        lang_beg = request.lang
        output_path = request.output_path

        if get_lang_name_to_tts_melo(lang_beg):
            speed = 0.65
            if os_name == 'Linux':
                device_melo = 'cuda:0'
            if os_name == 'Darwin':
                device_melo = 'mps'

            lang = get_lang_name_to_tts_melo(lang_beg)
            speaker = get_speaker_name_to_tts_melo(lang)
            model_melo = TTS(language=lang, device=device_melo)
            speaker_ids = model_melo.hps.data.spk2id
            speaker_ids = speaker_ids[speaker]


        else:
            generate_and_play(text,'nova',path=output_path)
            lang = lang_beg



        if not text or not lang or not output_path:
            raise HTTPException(status_code=400, detail="text,lang,output_path is required")
        if get_lang_name_to_tts_melo(lang_beg):
            try:
                model_melo.tts_to_file(text, speaker_ids, output_path, speed=speed)
                playsound(output_path)

                return FileResponse(output_path, media_type="audio/wav", filename=output_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))





if GEN_IMAGE_SD3:
    from pydantic import BaseModel
    import torch
    from fastapi.responses import FileResponse
    from diffusers import StableDiffusion3Pipeline

    pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers",
                                                    torch_dtype=torch.float16,device='cuda:0')
    pipe = pipe.to("cuda:0")


    class ImageRequest(BaseModel):
        prompt: str
        negative_prompt: str
        num_inference_steps: int


    @app.post("/generate_image/")
    async def generate_image(request: ImageRequest):
        try:
            image = pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                num_inference_steps=request.num_inference_steps,
                guidance_scale=7.0,
                height=512,
                width=512
            ).images[0]
            file_path = "pic.png"
            image.save(file_path)
            return FileResponse(file_path, media_type="image/png", filename="pic.png")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if TRANSLATE_NLLB:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

    checkpoint = "facebook/nllb-200-distilled-600M"
    model_trans = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)



    class TranslationRequest(BaseModel):
        text: str
        source_language: str
        target_language: str


    class TranslationResponse(BaseModel):
        translated_text: str


    @app.post("/translate", response_model=TranslationResponse)
    def translate(request: TranslationRequest):
        translator = pipeline('translation', model=model_trans, tokenizer=tokenizer,src_lang=request.source_language, tgt_lang=request.target_language,
                              max_length=400, device='cuda:0')
        translated_text = translator(request.text)[0]['translation_text']
        return TranslationResponse(translated_text=translated_text)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
