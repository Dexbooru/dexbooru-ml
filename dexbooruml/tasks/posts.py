from dexbooruml.config.celery_config import celery_app
from dexbooruml.config.weaviate_config import vectordb_client, POST_IMAGE_COLLECTION_NAME
from dexbooruml.utilities.files import url_to_base64
from weaviate.util import generate_uuid5


@celery_app.task(ignore_result=True, rate_limit='100/m')
def insert_post_to_vectordb(post_id: str, image_urls: list[str]):
    objects: list[dict[str, str]] = []
    for image_url in image_urls:
        try:
            image_base64 = url_to_base64(image_url)
            objects.append(
                {'postId': post_id, 'blob': image_base64, 'imageUrl': image_url})
        except Exception as e:
            pass

    post_collection = vectordb_client.collections.get(
        POST_IMAGE_COLLECTION_NAME)
    with post_collection.batch.dynamic() as batch:
        for object in objects:
            object_uuid = generate_uuid5(object)
            batch.add_object(properties=object, uuid=object_uuid)
