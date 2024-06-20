from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

GEN_IMAGE_SD3 = False
TRANSLATE_NLLB = True
STT_WHISPERX = True
TTS_MELO = True

app = FastAPI()

if GEN_IMAGE_SD3:
    from pydantic import BaseModel
    import torch
    from fastapi.responses import FileResponse
    from diffusers import StableDiffusion3Pipeline

    pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers",
                                                    torch_dtype=torch.float16)
    pipe = pipe.to("cuda")


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
            ).images[0]
            file_path = "pic.png"
            image.save(file_path)
            return FileResponse(file_path, media_type="image/png", filename="pic.png")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if STT_WHISPERX:
    import whisperx

    model = whisperx.load_model("large-v3", device="cuda")


    class TranscribeResponse(BaseModel):
        transcribe_text: str


    @app.post("/transcribe/")
    async def transcribe(file: UploadFile = File(...)):

        audio = whisperx.load_audio(file.filename)

        result = model.transcribe(audio, batch_size=16, task="transcribe",language="en")

        transcription = ''
        for segment in result['segments']:
            transcription += ("[%.2fs -> %.2fs] %s" % (segment['start'], segment['end'], segment['text']))

        return TranscribeResponse(transcribe_text=transcription)

if TTS_MELO:
    from melo.api import TTS
    from fastapi.responses import FileResponse
    from LANG_CODES import get_lang_name_to_tts_melo


    class TextRequest(BaseModel):
        text: str
        lang: str
        output_path: str


    @app.post("/tts_melo")
    async def tts_melo(request: TextRequest):
        text = request.text
        lang = request.lang
        output_path = request.output_path




        speed = 0.9
        device_melo = 'cuda:0'
        lang, speaker = get_lang_name_to_tts_melo(lang)
        model_melo = TTS(language=lang, device=device_melo)
        speaker_ids = model_melo.hps.data.spk2id
        speaker_ids = speaker_ids[speaker]

        current_lang = lang.upper()
        melo_lang = model_melo.language

        if current_lang != melo_lang:
            lang, speaker = get_lang_name_to_tts_melo(lang)
            speed = 0.9
            device_melo = 'cuda:0'
            model_melo = TTS(language=lang, device=device_melo)
            speaker_ids = model_melo.hps.data.spk2id
            speaker_ids = speaker_ids[speaker]



        if not text or not lang or not output_path:
            raise HTTPException(status_code=400, detail="text,lang,output_path is required")

        try:
            model_melo.tts_to_file(text, speaker_ids, output_path, speed=speed)

            return FileResponse(output_path, media_type="audio/wav", filename=output_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if TRANSLATE_NLLB:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    from LANG_CODES import get_lang_name_to_nllb

    checkpoint = 'facebook/nllb-200-distilled-600M'
    model_trans = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    translator = pipeline('translation', model=model_trans, tokenizer=tokenizer, src_lang='en', tgt_lang="spa_Latn",
                          max_length=400)


    class TranslationRequest(BaseModel):
        text: str
        target_language: str


    class TranslationResponse(BaseModel):
        translated_text: str


    @app.post("/translate", response_model=TranslationResponse)
    def translate(request: TranslationRequest):
        translated_text = translator(request.text)[0]['translation_text']
        return TranslationResponse(translated_text=translated_text)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
