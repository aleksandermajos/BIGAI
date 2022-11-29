from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch

class StableDiffiusion():

    def __init__(self,model_id):
        scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, revision="fp16",torch_dtype=torch.float16)
        self.pipe = self.pipe.to("cuda")
        self.path = "../../ALOHAPP/DATA/PIC/"

    def askModel(self,prompt,h=768,w=768):
        image = self.pipe(prompt, height=h, width=w).images[0]
        return image

    def ask_and_save(self,prompt,file,h=768,w=768):
        image = self.askModel(prompt,h=h,w=w)
        image.save(self.path+file)
