from functions_modelling import *
import os
import time

# Let's create a custom model so we can fine tune it.
model_id = create_model("Sample")

# We now upload the images to fine tune this model.
upload_image_samples(model_id)

# Now it's time to fine tune the model. Notice how I'm continuously 
# getting the status of the training job and waiting until it's
# finished before moving on.
version_id, status = queue_training_job(model_id)
while status != "finished":
    time.sleep(10)
    version_id, status = get_model_version(model_id, version_id)

os.environ['MODEL_ID'] = model_id