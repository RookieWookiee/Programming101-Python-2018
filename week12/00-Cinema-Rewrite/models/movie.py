from sqlalchemy import (
    Column, String, Integer,
    Float, Date, Time,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from models.base_model import Base

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    rating = Column(Float)

class Projection(Base):
    __tablename__ = 'projections'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    movie_id = Column(Integer, ForeignKey(Movie.id))
    movie = relationship(Movie, backref="movies")
    date = Column(Date)
    time = Column(Time)
