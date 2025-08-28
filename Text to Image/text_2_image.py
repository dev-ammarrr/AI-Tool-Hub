from diffusers import StableDiffusionPipeline
import torch

# Load the Stable Diffusion pipeline (this will download the model the first time)
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)
if torch.cuda.is_available():
    pipe = pipe.to("cuda")

# Your text prompt
prompt = "a magical forest at sunset, with glowing mushrooms and fireflies, a small wooden bridge over a crystal clear stream, photorealistic, cinematic lighting, 8k resolution"

# Generate image
image = pipe(prompt).images[0]

# Save the image
image.save("generated_image new.png")
print("Image saved as generated_image new.png")
