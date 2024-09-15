import torch
from diffusers import DiffusionPipeline
from transformers import T5EncoderModel, BitsAndBytesConfig

#https://huggingface.co/black-forest-labs/FLUX.1-dev
#https://huggingface.co/docs/diffusers/en/api/pipelines/flux
#https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/flux/pipeline_flux.py

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model_id = "black-forest-labs/FLUX.1-dev"    #needs 4 steps only - it is faster than the dev version as the name implies
import torch
from huggingface_hub import hf_hub_download
from diffusers import FluxTransformer2DModel, DiffusionPipeline

dtype, device = torch.bfloat16, "cuda:0"
ckpt_id = "black-forest-labs/FLUX.1-schnell"

with torch.device("meta"):
    config = FluxTransformer2DModel.load_config(ckpt_id, subfolder="transformer")
    model = FluxTransformer2DModel.from_config(config).to(dtype)

ckpt_path = hf_hub_download(repo_id="sayakpaul/flux.1-schell-int8wo", filename="flux_schnell_int8wo.pt")
state_dict = torch.load(ckpt_path, map_location="cuda:0")
model.load_state_dict(state_dict, assign=True)

pipeline = DiffusionPipeline.from_pretrained(ckpt_id, transformer=model, torch_dtype=dtype).to("cuda:0")
image = pipeline(
	"cat", guidance_scale=0.0, num_inference_steps=4, max_sequence_length=256
).images[0]
image.save("flux_schnell_int8.png")