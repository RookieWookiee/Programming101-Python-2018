from models.movie import Movie, Projection
from db_layer.session import Session


class MovieController:
    @classmethod
    def get_all(cls):
        session = Session()
        return session.query(Movie).order_by(Movie.rating.desc()).all()

    @classmethod
    def get_all_projections_by_date(cls, movie_id, date):
        session = Session()
        query = session.query(Projection).filter(Projection.movie_id == movie_id)

        if date is not None:
            query = query.filter(Projection.date == date)

        return query.order_by(Projection.date, Projection.time).all()
    
    @classmethod
    def get_by_id(cls, movie_id):
        session = Session()
        return session.query(Movie).filter(Movie.id == movie_id).one()


class ProjectionController:
    @classmethod
    def get_by(cls, **kwargs):
        if len(kwargs) != 1:
            raise ValueError(f'Expected 1 argument, got {len(kwargs)}')

        by = next(iter(kwargs))
        if not hasattr(Projection, by):
            raise ValueError(f'Projection has not {by} attribute')

        session = Session()

        response = session.query(Projection).filter(getattr(Projection, by) == kwargs[by]).all()
        return response[0] if len(response) == 1 else response
