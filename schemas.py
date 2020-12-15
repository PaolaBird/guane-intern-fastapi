from pydantic import BaseModel


class Dog(BaseModel):
    id: int
    name: str
    picture: str
    created_date: str
    is_adopted: bool
    id_user: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    apellido: str
    email: str

    class Config:
        orm_mode = True
