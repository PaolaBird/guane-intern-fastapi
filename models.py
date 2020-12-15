from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

from database import Base


class Dog(Base):
    __tablename__ = "dog"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    picture = Column(String(255))
    created_date = Column(String(255))
    is_adopted = Column(Boolean)
    id_user = Column(Integer, ForeignKey('user.id'), primary_key=True)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    apellido = Column(String(255))
    email = Column(String(255))
