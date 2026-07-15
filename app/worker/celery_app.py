from celery import Celery

from app.core.config import settings


celery = Celery(
    "price_tracker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


celery.conf.update(

    task_serializer="json",

    accept_content=[
        "json",
    ],

    result_serializer="json",


    timezone="UTC",

    enable_utc=True,


    task_routes={
        "app.tasks.*": {
            "queue": "prices",
        },
    },


    task_ignore_result=True,


    task_acks_late=True,

    worker_prefetch_multiplier=1,


    beat_schedule={

        "check-products-every-hour": {

            "task": "app.tasks.check_all_prices",

            "schedule": 3600,

        },

    },
)


celery.autodiscover_tasks(
    [
        "app.tasks",
    ],
)