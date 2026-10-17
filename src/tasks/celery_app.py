from celery import Celery
from celery.schedules import crontab
import os


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

celery_app = Celery(
    "deribit_worker",
    broker=REDIS_URL,
    include=["src.tasks.worker"] 
)


celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "src.tasks.worker.fetch_and_save_prices",
        "schedule": crontab(minute="*"),
    }
}
celery_app.conf.timezone = "UTC"