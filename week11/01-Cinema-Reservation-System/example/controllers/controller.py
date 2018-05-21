from .movie_controller import MovieController


class Controller:

    @classmethod
    def create_movie(cls, name, rating):
        # Check user is logged in
        return MovieController.create(name, rating)

    def show_movies(cls):
        # Check user is logged in
        return MovieController.show_all_movies()
