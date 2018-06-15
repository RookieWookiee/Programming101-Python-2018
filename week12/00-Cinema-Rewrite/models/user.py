from models.base_model import Base
from models.movie import Projection
from sqlalchemy import (
    Column, String, Integer,
    Float, Date, Time, ForeignKey
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    salt = Column(String)


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))

    projection_id = Column(Integer, ForeignKey(Projection.id))
    user = relationship('User', backref='reservations')
    row = Column(Integer)
    col = Column(Integer)
