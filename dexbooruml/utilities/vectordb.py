import weaviate

class VectorDatabase:
    client: weaviate.WeaviateClient

    def __init__(client: weaviate.WeaviateClient):
        self.client = client

    