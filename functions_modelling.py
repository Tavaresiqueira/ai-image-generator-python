import requests
import json
import boto3
import os


API_KEY = os.getenv('API_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}


s3 = boto3.resource('s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)
bucket = s3.Bucket('authetication-images')

keys = []

for obj in bucket.objects.all():
    keys.append(obj.key)




IMAGES = []
s3 = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)

# Defina o nome do seu bucket e do arquivo
bucket_name = 'authetication-images'
file_names = keys
for file_name in file_names:
  # Gere a URL pública com uma validade de 1 hora (3600 segundos)
  url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)
  IMAGES.append(url)
  # Use a URL pública diretamente em seu código


def create_model(title):
    url = "https://api.tryleap.ai/api/v1/images/models"

    payload = {
        "title": title,
        "subjectKeyword": "@me"
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    model_id = json.loads(response.text)["id"]
    return model_id


def upload_image_samples(model_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/samples/url"

    payload = {"images": IMAGES}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.status_code


def queue_training_job(model_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/queue"
    response = requests.post(url, headers=HEADERS)
    print(response.text)
    data = json.loads(response.text)

    

    version_id = data["id"]
    status = data["status"]

    print(f"Version ID: {version_id}. Status: {status}")

    return version_id, status


def get_model_version(model_id, version_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/versions/{version_id}"
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)

    version_id = data["id"]
    status = data["status"]

    print(f"Version ID: {version_id}. Status: {status}")

    return version_id, status


def generate_image(model_id, prompt):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences"

    payload = {
        "prompt": prompt,
        "steps": 50,
        "width": 512,
        "height": 512,
        "numberOfImages": 1,
        "seed": 4523184
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    print(response.status_code)
    data = json.loads(response.text)

    inference_id = data["id"]
    status = data["status"]

    print(f"Inference ID: {inference_id}. Status: {status}")

    return inference_id, status


def get_inference_job(model_id, inference_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences/{inference_id}"

    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)

    inference_id = data["id"]
    state = data["state"]
    image = None

    if len(data["images"]):
        image = data["images"][0]["uri"]

    print(f"Inference ID: {inference_id}. State: {state}")

    return inference_id, state, image


