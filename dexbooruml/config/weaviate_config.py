import os
import weaviate
from dotenv import load_dotenv
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import Property, DataType, Configure

load_dotenv()

POST_IMAGE_COLLECTION_NAME = 'Posts'
POST_IMAGE_COLLECTION_DESCRIPTION = 'indexed post images from Dexbooru for image similarity search'

vectordb_client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_params(
        http_host=os.getenv("WEAVIATE_HTTP_HOST"),
        http_port=os.getenv("WEAVIATE_HTTP_PORT"),
        http_secure=os.getenv('SERVER_ENV') == 'production',
        grpc_host=os.getenv("WEAVIATE_GRPC_HOST"),
        grpc_port=os.getenv("WEAVIATE_GRPC_PORT"),
        grpc_secure=os.getenv('SERVER_ENV') == 'production',
    ),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120), 
    ),
    skip_init_checks=False
)

vectordb_client.connect()

if not vectordb_client.collections.exists(POST_IMAGE_COLLECTION_NAME):
    vectordb_client.collections.create(
        name=POST_IMAGE_COLLECTION_NAME, 
        description=POST_IMAGE_COLLECTION_DESCRIPTION,
        properties=[
            Property(name='postId', data_type=DataType.UUID, skip_vectorization=True),
            Property(name='imageUrl', data_type=DataType.TEXT, skip_vectorization=True),
            Property(name='blob', data_type=DataType.BLOB),
        ],
        vector_index_config=Configure.VectorIndex.hnsw(),
        vectorizer_config=Configure.Vectorizer.img2vec_neural(image_fields=['blob']),
    )