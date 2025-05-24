from fastapi import APIRouter, status, Depends
from schema.users import UserCreate, UserUpdate
from db.dep import get_db
from sqlalchemy.orm import Session
from crud.users import (
    create_user, 
    get_user, 
    get_users,
    update_user,
    user_delete
    )
from uuid import UUID


router = APIRouter()

@router.post("/create")
def create(user: UserCreate, db: Session = Depends(get_db)):
    resp = create_user(db=db, user_create=user)
    return resp


@router.get("/get/{user_id}")
def user_get(user_id: UUID, db: Session = Depends(get_db)):
    resp = get_user(user_id=user_id, db=db)
    return resp

@router.get("/getAll")
def users_get_all(db: Session = Depends(get_db)):
    resp = get_users(db=db)
    return resp


@router.patch("/update/{user_id}")
def user_update(
    user_id: UUID, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db)
    ):
    resp = update_user(db=db, user_id=user_id, user_update=user_update)
    return resp


@router.delete("/delete")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    resp = user_delete(user_id=user_id, db=db)
    return resp
