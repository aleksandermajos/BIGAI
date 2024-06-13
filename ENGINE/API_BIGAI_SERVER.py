from fastapi import FastAPI, File, UploadFile, HTTPException

generate_image = True
translate = False
STT = False
TTS_ = False

app = FastAPI()

if generate_image:
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


if STT:
    import whisperx
    model = whisperx.load_model("large-v3", device="cuda")

    class TranscribeResponse(BaseModel):
        transcribe_text: str


    @app.post("/transcribe/")
    async def transcribe(file: UploadFile = File(...)):

        audio = whisperx.load_audio(file.filename)

        result = model.STT(audio, batch_size=16, task="transcribe", language='en')

        transcription = ''
        for segment in result['segments']:
            transcription += ("[%.2fs -> %.2fs] %s" % (segment['start'], segment['end'], segment['text']))

        return TranscribeResponse(transcribe_text=transcription)

if TTS_:
    from melo.api import TTS
    speed = 0.9
    device_melo = 'cuda:0'
    model_melo = TTS(language='EN', device=device_melo)
    speaker_ids = model_melo.hps.data.spk2id






if translate:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
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