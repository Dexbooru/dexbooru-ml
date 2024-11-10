import base64
import requests
from fastapi import UploadFile

VALID_IMAGE_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/jpg', 'png', 'webp', 'jpg', 'jpeg', 'gif'] 

def file_to_base64(file: UploadFile) -> str:
    content = file.file.read()
    return base64.b64encode(content).decode("utf-8")

def is_content_type_image(content_type: str) -> bool:
    return content_type.lower() in VALID_IMAGE_CONTENT_TYPES or any(content_type.lower().startswith(image_type) for image_type in VALID_IMAGE_CONTENT_TYPES)

def url_to_base64(url: str) -> str:
    image_response = requests.get(url)  
    if not is_content_type_image(image_response.headers.get('content-type')):
        raise ValueError('Invalid image type')

    content = image_response.content
    return base64.b64encode(content).decode("utf-8")

