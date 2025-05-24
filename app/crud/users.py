from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.users import Users
from schema.users import UserCreate, UserUpdate
from uuid import UUID


def create_user(db: Session, user_create: UserCreate):
    db_user = Users(name=user_create.name, email=user_create.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: UUID):
    return db.query(Users).filter(Users.id == user_id).first()

def get_users(db: Session):
    return db.query(Users).all()

def update_user(db: Session, user_id: UUID, user_update: UserUpdate):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
    
    if user_update.name:
        user.name = user_update.name
    
    if user_update.email:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user


def user_delete(user_id: UUID, db: Session):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
    
    db.delete(user)
    db.commit()
    return {"OK": True, "details": f"user {user.name} has been deleted"}

    

    
