from OmniGen import OmniGenPipeline

pipe = OmniGenPipeline.from_pretrained("Shitao/OmniGen-v1")
# Note: Your local model path is also acceptable, such as 'pipe = OmniGenPipeline.from_pretrained(your_local_model_path)', where all files in your_local_model_path should be organized as https://huggingface.co/Shitao/OmniGen-v1/tree/main
# Note: If the original link https://huggingface.co/Shitao/OmniGen-v1/tree/main is unstable when downloading, it is recommended to use this mirror link https://hf-mirror.com/Shitao/OmniGen-v1/tree/main or other ways in https://hf-mirror.com/

## Text to Image
images = pipe(
    prompt="Portrait of a young woman with freckles, natural look",
    height=1024,
    width=1024,
    guidance_scale=2.5,
    seed=0,
)
images[0].save("example_t2i.png")  # save output PIL Image

## Multi-modal to Image
# In the prompt, we use the placeholder to represent the image. The image placeholder should be in the format of <img><|image_*|></img>
# You can add multiple images in the input_images. Please ensure that each image has its placeholder. For example, for the list input_images [img1_path, img2_path], the prompt needs to have two placeholders: <img><|image_1|></img>, <img><|image_2|></img>.
images = pipe(
    prompt="A woman in a black shirt is reading a book. The man is the right man in <img><|image_1|></img>.",
    input_images=["example_t2i.png"],
    height=1024,
    width=1024,
    guidance_scale=2.5,
    img_guidance_scale=1.6,
    seed=0
)
images[0].save("example_ti2i.png")  # save output PIL image