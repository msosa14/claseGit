from typing import List, Dict

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World this is my new API!"}

@app.get("/myname/{name}")
async def myName(name: str):
    return {"message": f"Hello {name} this is my new API!"}

@app.get("/myfullname/{name}")
async def myFullName(name: str):
    return {"message": f"Hello my full name is {name}."}

@app.get("/technology")
async def redirect_typer():
    return RedirectResponse("https://images.pexels.com/photos/5380651/pexels-photo-5380651.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")

@app.post("/users/create", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/{user_id}/", response_model=schemas.UserBase)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)


@app.post("/users/", response_model=List[schemas.UserData])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)
