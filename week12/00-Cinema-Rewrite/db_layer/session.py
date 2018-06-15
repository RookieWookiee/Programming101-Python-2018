from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///cinema.db')
Session = sessionmaker(bind=engine)
