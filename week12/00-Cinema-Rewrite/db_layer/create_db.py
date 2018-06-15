from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.user import *
from models.movie import *
from db_layer.session import engine

from datetime import time, date

Base.metadata.create_all(engine)
