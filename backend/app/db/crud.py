from sqlalchemy.orm import Session
import models.models as models
import schemas.schemas as schemas
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from jose import jwt
from config import settings
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class Hasher:
    # TO_CREATE_HASH_PASSWORD
    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)

    # TO_VERIFY
    @staticmethod
    def verify_password(plain_password, hash_password):
        try:
            if pwd_context.verify(plain_password, hash_password) == True:
                return "OK"
            else:
                return "BAD"
        except:
            ValueError
            return "BAD"


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = Hasher.get_hash_password(f"{user.password}")
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not existing_user:
        return {"message": f"No Details found for User ID {user_id}"}
    email = user.email
    fake_hashed_password = Hasher.get_hash_password(f"{user.password}")
    # existing_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    existing_user.email = email
    existing_user.hashed_password = fake_hashed_password
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    # existing_user.update(jsonable_encoder(user))  
    return user

def delete_user(db: Session, user_id):
    existing_user = db.query(models.User).filter(models.User.id == user_id)
    if not existing_user.first():
        return {"message": f"No Details found for User ID {user_id}"}
    existing_user.delete()
    db.commit()
    return {"message": f"User id {user_id} has been succesfully deleted"}


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item: schemas.ItemBase, item_id: int, owner_id: int):
    existing_item = db.query(models.Item).filter(models.Item.id == item_id)
    if not existing_item.first():
        return {"message": f"No Details found for Item ID {item_id}"}
    if existing_item.first().owner_id == owner_id:
        existing_item.update(jsonable_encoder(item))
        db.commit()
    return item

def delete_item(db: Session, item_id: int):
    existing_item = db.query(models.Item).filter(models.Item.id == item_id)
    if not existing_item.first():
        return {"message": f"No Details found for Item ID {item_id}"}
    existing_item.delete()
    db.commit()
    return {"message": f"Item id {item_id} has been succesfully deleted"}

def delete_all_items_by_user_id(db: Session, user_id: int):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not existing_user:
        return {"message": f"No Details found for User ID {user_id}"}
    # existing_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    existing_user.items = []
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    # existing_user.update(jsonable_encoder(user))  
    return {"DELETED"}


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_user_from_token(db, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(models.User).filter(models.User.email==username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
    return user
