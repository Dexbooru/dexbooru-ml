import os
from celery import Celery
from dotenv import load_dotenv
from celery.signals import worker_shutdown
from dexbooruml.config.weaviate_config import vectordb_client

load_dotenv()

celery_app = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))

celery_app.conf.update(
    imports=['dexbooruml.tasks.posts'],
    broker_connection_retry_on_startup=True,
    task_track_started=True
)

@worker_shutdown.connect
def shutdown_worker(**kwargs):
    vectordb_client.close()