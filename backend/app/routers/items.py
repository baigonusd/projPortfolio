from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
import db.crud as crud
import schemas.schemas as schemas
from sqlalchemy.orm import Session
from db.database import get_db
from models.models import Item
from routers.login import oauth2_scheme


router = APIRouter()

# ITEM_CREATE


@router.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(item: schemas.ItemCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = crud.get_user_from_token(db, token)
    # db_user = crud.get_user(db, user_id=user_id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_item(db=db, item=item, user_id=user.id)

# LIST_OF_ITEM


@router.get("/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# READ ITEM

@router.get("/item/{id}", response_model=schemas.Item, tags=["Items"])
def read_item_by_id(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# UPDATE ITEM

@router.put("/item/update/{id}", tags=["Items"])
def update_item_by_id(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
    user = crud.get_user_from_token(db, token)
    existing_item = db.query(Item).filter(Item.id==item_id)
    if not existing_item.first():
        return {"message": "No details exists for Item ID {item_id}"}
    if existing_item.first().owner_id == user.id:
        item_to_update = crud.update_item(db, item, item_id=existing_item.first().id, owner_id=user.id)
        return item_to_update
    else:
        return {"message": "You don't have a permission for updating this item"}

# DELETE ITEM

@router.delete("/item/delete/{id}", tags=["Items"])
def delete_item_by_id(item_id: int, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
    user = crud.get_user_from_token(db, token)
    existing_item = db.query(Item).filter(Item.id==item_id)
    if not existing_item.first():
        return {"message": "No details exists for Item ID {item_id}"}
    if existing_item.first().owner_id == user.id:
        deleted_item = crud.delete_item(db, item_id=existing_item.first().id)
        return deleted_item
    else:
        return {"message": "You don't have a permission for deleting this item"}
    