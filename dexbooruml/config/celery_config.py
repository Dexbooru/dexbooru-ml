import os
from celery import Celery
from dotenv import load_dotenv
from dexbooruml.config.weaviate_config import vectordb_client

load_dotenv()
_celery_app = None

def get_celery_app():
    global _celery_app
    
    if _celery_app is None:
        _celery_app = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))
        _celery_app.conf.update(
            imports=['dexbooruml.tasks.posts'],
            broker_connection_retry_on_startup=True,
            task_track_started=True
        )

    return _celery_app  


celery_app = get_celery_app()
