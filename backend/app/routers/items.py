from typing import List
from fastapi import Depends, APIRouter, HTTPException
import db.crud as crud
import schemas.schemas as schemas
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.encoders import jsonable_encoder
from models.models import Item

router = APIRouter()

# ITEM_CREATE


@router.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# LIST_OF_ITEM


@router.get("/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# UPDATE ITEM

@router.put("/item/update/{id}", tags=["Items"])
def update_item(item_id: int, owner_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    item_to_update = crud.update_item(db, item, item_id=item_id, owner_id=owner_id)
    if item_to_update is None:
        raise HTTPException(status_code=404, detail="Item or owner not found")
    return item_to_update