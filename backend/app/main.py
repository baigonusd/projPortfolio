from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

import db.crud as crud
import models.models as models
import schemas.schemas as schemas
from db.database import Base, engine, get_db
from config import settings

from models.models import Order
# from celery_worker import create_order
from routers import users, items

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    contact=settings.CONTACT,
    openapi_tags=settings.TAGS
)


app.include_router(users.router)
app.include_router(items.router)
# Dependency


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post('/order')
# def add_order(order: Order):
#     # use delay() method to call the celery task
#     create_order.delay(order.customer_name, order.order_quantity)
#     return {"message": "Order Received! Thank you for your patience."}

@app.get('/getenvvar', tags=["config"])
def get_envvars():
    return {"database": settings.DATABASE_URL}

# CREATING_USER


# @app.post("/users/", response_model=schemas.User, tags=["Users"])
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

# USER_LIST


# @app.get("/users/", response_model=List[schemas.User], tags=["Users"])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
    # elif skip < 0 or limit <= 0:
    #     return {"ERROR": "Values have to be positive"}
    # else:
    #     return {"ERROR": "First value cannot be more than second"}

# USER_INFO


# @app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# ITEM_CREATE


# @app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["Items"])
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)

# LIST_OF_ITEM


# @app.get("/items/", response_model=List[schemas.Item], tags=["Items"])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
