from typing import List

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/dogs/", response_model=List[schemas.Dog])
def show_dogs(request: Request, name: str = None, is_adopted: bool = None, db: Session = Depends(get_db)):
    dogs = {}
    queries = request.url.query.split('&')
    kwargs = {}
    if len(queries) == 1 and queries[0] != '':
        for query in queries:
            query = query.split('=')
            kwargs.update({query[0]: query[1]})
            if query[0] == 'name':
                dogs = db.query(models.Dog).filter(models.Dog.name == query[1]).all()
            elif query[0] == 'is_adopted':
                dogs = db.query(models.Dog).filter(models.Dog.is_adopted == query[1]).all()
    elif len(queries) >= 2:
        dogs = db.query(models.Dog).filter(models.Dog.name == name and models.Dog.is_adopted == is_adopted).all()
    elif len(queries) == 1 and queries[0] == '':
        dogs = db.query(models.Dog).all()

    return dogs


@app.get("/dogs/{id}", response_model=schemas.Dog)
def show_dog(id: int, db: Session = Depends(get_db)):
    dog = db.query(models.Dog).filter(models.Dog.id == id).first()
    return dog


@app.post("/dogs/", response_model=schemas.Dog)
def create_dogs(dog: schemas.Dog, db: Session = Depends(get_db)):
    dog = models.Dog(id=dog.id, name=dog.name, picture=dog.picture, created_date=dog.created_date,
                     is_adopted=dog.is_adopted, id_user=dog.id_user)
    db.add(dog)
    db.commit()
    db.refresh(instance=dog)
    return dog


@app.put("/dogs/{id}", response_model=schemas.Dog)
def update_dogs(id: int, dog: schemas.Dog, db: Session = Depends(get_db)):
    dog = db.query(models.Dog).filter(models.Dog.id == id).update(
        {'id': dog.id, 'name': dog.name, 'picture': dog.picture, 'created_date': dog.created_date,
         'is_adopted': dog.is_adopted, 'id_user': dog.id_user})
    db.commit()
    return dog


@app.delete("/dogs/{id}")
def delete_dog(id: int, db: Session = Depends(get_db)):
    dog = db.query(models.Dog).filter(models.Dog.id == id).first()
    db.delete(instance=dog)
    db.commit()
    return "Eliminado éxitoso"


@app.get("/users/", response_model=List[schemas.User])
def show_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/users/{id}", response_model=schemas.User)
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@app.post("/users/", response_model=schemas.User)
def create_users(user: schemas.User, db: Session = Depends(get_db)):
    user = models.User(id=user.id, name=user.name, apellido=user.apellido, email=user.email)
    db.add(user)
    db.commit()
    db.refresh(instance=user)
    return user


@app.put("/users/{id}", response_model=schemas.User)
def update_users(id: int, user: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).update(
        {'id': user.id, 'name': user.name, 'apellido': user.apellido, 'email': user.email})
    db.commit()
    return user


@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    db.delete(instance=user)
    db.commit()
    return "Borrado éxitoso"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
