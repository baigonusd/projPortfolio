from re import L
from typing import List
from fastapi import Depends, APIRouter, HTTPException
import db.crud as crud
import schemas.schemas as schemas
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

# CREATING_USER


@router.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    check_user = crud.check_user(user)
    if check_user is False:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# USER_LIST


@router.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
    # elif skip < 0 or limit <= 0:
    #     return {"ERROR": "Values have to be positive"}
    # else:
    #     return {"ERROR": "First value cannot be more than second"}

# USER_INFO


@router.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# USER_UPDATE

@ router.put("/user/update/{id}", tags=["Users"])
def update_user_by_id(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_update = crud.update_user(db, user, user_id=user_id)
    if user_update is False:
        raise HTTPException(status_code=400, detail="Old password doesn't match")
    check_user = crud.check_user(user)
    if check_user is False:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    return user_update

# USER_DELETE

@router.delete("/user/delete/{id}", tags=["Users"])
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    crud.delete_all_items_by_user_id(db, user_id)
    deleted_user = crud.delete_user(db, user_id)
    return deleted_user
