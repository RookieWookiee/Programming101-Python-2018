from database_layer.models import MovieModel


class MovieController:
    movie = MovieModel()

    @classmethod
    def create(cls, name, rating):
        if int(rating) < 0:
            raise ValueError("Rating must be positive number")
        # all_movies_names = MovieModel.list(values_list='name')

        cls.movie.create(name, rating)

    @classmethod
    def show_all_movies(cls):
        print(cls.movie.list())
