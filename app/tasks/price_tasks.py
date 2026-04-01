from app.worker.celery_app import celery


@celery.task
def parse_price(product_id: int):
    # тут будет парсинг сайта
    print(f"Parsing price for product {product_id}")