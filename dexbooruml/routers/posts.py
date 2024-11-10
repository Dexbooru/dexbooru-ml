from fastapi import APIRouter, File, UploadFile
from dexbooruml.tasks.posts import insert_post_to_vectordb
from dexbooruml.config.weaviate_config import vectordb_client, POST_IMAGE_COLLECTION_NAME
from dexbooruml.utilities.files import url_to_base64, file_to_base64
from pydantic import BaseModel, UUID4, AfterValidator, HttpUrl, Field, model_validator, field_validator
from typing import Annotated, Optional
from weaviate.classes.query import MetadataQuery
import uuid

MIN_K = 1
MAX_K = 40
DEFAULT_K = 10


class PostIndexInput(BaseModel):
    post_id: Annotated[UUID4, Field(
        description="Unique identifier for the post")]
    image_urls: list[HttpUrl]

    @field_validator('post_id', mode='before')
    def validate_post_id(cls: any, value: UUID4) -> UUID4:
        if not value:
            return uuid.uuid4()
        return value

    @field_validator('image_urls', mode='before')
    def validate_image_urls(cls: any, value: list[HttpUrl]) -> list[HttpUrl]:
        if not value:
            raise ValueError("At least one image URL must be provided.")
        return value


class PostIndexOutput(BaseModel):
    status: str
    task_id: str


class PostSimilarityInput(BaseModel):
    image_url: Optional[HttpUrl] = Field(
        default=None, description="An image URL")
    image_file: Optional[str] = Field(
        default=None,
        description="Image file represented in base 64 form")
    k: int = Field(
        default=DEFAULT_K, description="Number of similar results to retrieve")
    distance_threshold: float = Field(default=0.0, description="Distance threshold")

    @model_validator(mode='before')
    def validate_image_inputs(cls, values: dict) -> dict:
        if not values.get('image_url') and not values.get('image_file'):
            raise ValueError(
                "Either 'image_url' or 'image_file' must be provided.")

        k = values.get('k')
        if k < 1:
            raise ValueError("'k' must be greater than 0.")
        if k not in range(MIN_K, MAX_K + 1):
            raise ValueError(
                f"'k' must be between {MIN_K} and {MAX_K} inclusive.")

        return values


class PostSimilarityResult(BaseModel):
    post_id: uuid.UUID
    distance: float
    image_url: str


class PostSimilarityOutput(BaseModel):
    status: str
    results: list[PostSimilarityResult]


def register_endpoints(router: APIRouter):
    @router.post('/index', status_code=201, response_model=PostIndexOutput)
    def index_post_images(input: PostIndexInput):
        post_id = str(input.post_id) if not isinstance(
            input.post_id, str) else input.post_id
        image_urls = [str(url) for url in input.image_urls]

        task_response = insert_post_to_vectordb.delay(post_id, image_urls)
        task_id = task_response.id

        return {'status': 'success', 'task_id': task_id}

    @router.post('/index/similarity', status_code=200, response_model=PostSimilarityOutput)
    def find_similar_post_images(input: PostSimilarityInput):
        image_url = input.image_url
        image_file = input.image_file
        k = input.k

        image_base64: str = url_to_base64(
            image_url) if image_url else image_file

        post_collection = vectordb_client.collections.get(
            POST_IMAGE_COLLECTION_NAME)
        similarity_search_results = post_collection.query.near_image(
            near_image=image_base64,
            return_properties=['postId', 'imageUrl'],
            return_metadata=MetadataQuery(distance=True),
            limit=k
        )

        api_friendly_similarity_search_results = []
        for similarity_search_result in similarity_search_results.objects:
            result_distance = similarity_search_result.metadata.distance
            properties = similarity_search_result.properties
            post_id = properties['postId']
            image_url = properties['imageUrl']

            api_friendly_similarity_search_results.append({
                'post_id': post_id,
                'distance': result_distance,
                'image_url': image_url,
            })
        api_friendly_similarity_search_results.sort(
            key=lambda result: result['distance'])

        return {
            'status': 'success',
            'results': api_friendly_similarity_search_results
        }


def build_posts_router() -> tuple[APIRouter, str]:
    router = APIRouter()
    register_endpoints(router)

    return router, 'posts'
