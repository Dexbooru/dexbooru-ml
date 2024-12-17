from fastapi import APIRouter
from dexbooruml.tasks import posts
from dexbooruml.config.weaviate_config import vectordb_client
from dexbooruml.config.celery_config import celery_app

CELERY_PING_TIMEOUT_SECONDS = 5

def register_endpoints(router: APIRouter):
    @router.get('/health-check')
    def health_check():
        vector_db_alive = vectordb_client.is_live()
        celery_response = celery_app.control.ping(timeout=CELERY_PING_TIMEOUT_SECONDS)
        celery_healthy = bool(celery_response)  

        application_healthy = all([vector_db_alive, celery_healthy])
        
        return {
            'status': 'success',
            'application_healthy': application_healthy,
            'vector_db_alive': vector_db_alive,
            'celery_healthy': celery_healthy
        }


def build_general_router() -> tuple[APIRouter, str]:
    router = APIRouter()
    register_endpoints(router)

    return router, 'general'