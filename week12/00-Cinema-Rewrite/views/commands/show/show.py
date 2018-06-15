from views.commands.cli import show
from controllers.movie_controller import MovieController
from controllers.user_controller import ReservationController
from views import cli_framework
from datetime import datetime


@show.command('movies')
def show_movies():
    movies = MovieController.get_all()

    print('Current movies:')
    for i, m in zip(range(len(movies)), movies):
        print(f'[{m.id}] - {m.name} ({m.rating})')


@show.group('movie')
def show_movie_group():
    print('show movie group')


# TODO: implement catch keyword which wraps the callback
@show_movie_group.command('projections')
@cli_framework.argument('movie_id', type=int)
@cli_framework.flag('--date', default=None,
    callback=lambda x: datetime.strptime(x, '%Y-%m-%d').date()
)
def show_movie_projections(movie_id, date):
    projections = MovieController.get_all_projections_by_date(movie_id, date)
    movie = MovieController.get_by_id(movie_id)
    date_str = f' on date {date.strftime("%Y-%m:%d")}' if date is not None else ''

    print(f"Projections for movie '{movie.name}'{date_str}:")

    for p in projections:
        taken_spots = len(ReservationController.get_by_projection_id(p.id))
        available_spots = 10 * 10 - taken_spots
        date_str = p.date.strftime('%Y-%m-%d') + ' ' if date is None else ''
        hour_str = p.time.strftime('%H:%M')

        print(
            f'[{p.id}] - {date_str}{hour_str} ({p.type})'
            f' - {available_spots} spots available'
        )
