from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel, AutoencoderKL
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
import numpy as np

import torch

import cv2
from PIL import Image

prompt = "Urban Oasis.Amidst the city's hustle, a green oasis emerges in the morning light. Captured by a wide-angle lens, the image showcases the integration of nature in the urban landscape. The soft morning sunlight bathes the scene in tranquility, emphasizing the harmonious coexistence"
negative_prompt = "low quality, bad quality, sketches"

image = load_image("qr_up.jpeg")

# initialize the models and pipeline
controlnet_conditioning_scale = 0.55  # ile jest wyjsciowego obrazka,qr codu w naszym przypadku
controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16
)
vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet, vae=vae, torch_dtype=torch.float16
)
pipe.enable_model_cpu_offload()

# get canny image
image = np.array(image)
image = cv2.Canny(image, 100, 200)
image = image[:, :, None]
image = np.concatenate([image, image, image], axis=2)
canny_image = Image.fromarray(image)

# generate image
image = pipe(
    prompt, controlnet_conditioning_scale=controlnet_conditioning_scale, image=canny_image
).images[0]
image.save("geeks3.jpg")

'''
n_steps = 40
high_noise_frac = 0.8

refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=pipe.text_encoder_2,
    vae=pipe.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)
refiner.to("cuda")
image = refiner(
    prompt=prompt,
    num_inference_steps=n_steps,
    denoising_start=high_noise_frac,
    image=image,
).images[0]
image.save("geeks3.jpg")

'''