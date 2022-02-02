#26
from fastapi import FastAPI
from config import settings

from models.models import Order
# from celery_worker import create_order
from routers import users, items, login
from webapps.routers import items as web_items
from fastapi.staticfiles import StaticFiles

# Alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    contact=settings.CONTACT,
    openapi_tags=settings.TAGS
)

StaticFiles(directory="static")

# Dependency in db.database

app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
app.include_router(web_items.router)


# @app.post('/order')
# def add_order(order: Order):
#     # use delay() method to call the celery task
#     create_order.delay(order.customer_name, order.order_quantity)
#     return {"message": "Order Received! Thank you for your patience."}

@app.get('/getenvvar', tags=["config"])
def get_envvars():
    return {"database": settings.DATABASE_URL}

