from functions_modelling import generate_image, get_inference_job
import time
import os

model_id = os.getenv('MODEL_ID')



try:
    inference_id, status = generate_image(
        model_id, 
        prompt="8k portrait of @me, pop art style, incredibly detailed faces, wearing a colorful men's suit, 🎨🖌️, idol, ios"
    )
    while status != "finished":
        time.sleep(10)
        inference_id, status, image = get_inference_job(model_id, inference_id)

    print(image)
except Exception as e:
    raise e








