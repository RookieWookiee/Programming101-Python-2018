from db_layer.session import Session
from models.movie import Movie, Projection
from models.user import User, Reservation
from datetime import date, time


def populate():
    session = Session()

    movies = [
        Movie(name='The Hunger Games: Catching Fire', rating=7.9),
        Movie(name='Wreck-It Ralph', rating=7.8),
        Movie(name='Her', rating=8.3)
    ]
    
    projections = [
        # date = datetime.strptime('2014-04-01', '%Y-%m-%d').[date() | time()]
        Projection(movie_id=1, type='3D', date=date(2014, 4, 1), time=time(hour=19, minute=10)),
        Projection(movie_id=1, type='2D', date=date(2014, 4, 1), time=time(hour=19, minute=0)),
        Projection(movie_id=1, type='4DX', date=date(2014, 4, 2), time=time(hour=21, minute=0)),
        Projection(movie_id=3, type='2D', date=date(2014, 4, 5), time=time(hour=20, minute=20)),
        Projection(movie_id=2, type='3D', date=date(2014, 4, 2), time=time(hour=22, minute=0)),
        Projection(movie_id=2, type='3D', date=date(2014, 4, 2), time=time(hour=19, minute=30)),
    ]

    reservations = [
        Reservation(user_id=3, projection_id=1, row=2, col=1),
        Reservation(user_id=3, projection_id=1, row=3, col=5),
        Reservation(user_id=3, projection_id=1, row=7, col=8),
        Reservation(user_id=2, projection_id=3, row=1, col=1),
        Reservation(user_id=2, projection_id=3, row=1, col=2),
        Reservation(user_id=5, projection_id=5, row=2, col=3),
        Reservation(user_id=6, projection_id=5, row=2, col=4),
    ]

    session.add_all(movies)
    session.add_all(projections)
    session.add_all(reservations)

    session.commit()

if __name__ == '__main__':
    populate()
