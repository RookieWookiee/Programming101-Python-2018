from views.commands.cli import make
from views import cli_framework
from views.commands.show.show import show_movies, show_movie_projections
from utils.decorators import interruptable
from db_layer.session import Session

from controllers.user_controller import user_logged_in, ReservationController, UserController
from controllers.movie_controller import MovieController, ProjectionController
from models.user import Reservation

from copy import deepcopy

ROWS = ReservationController.ROWS
COLS = ReservationController.COLS


@make.command('reservation')
@cli_framework.pass_env
@user_logged_in
@interruptable
def make_reservation(username):
    user = UserController.get_by(username=username)

    tickets = int(input('Number of tickets: '))
    show_movies()
    movie_id = input('Choose movie by id: ')
    show_movie_projections(movie_id, None)
    projection_id = input('Choose projection by id: ')

    projection = ProjectionController.get_by(id=projection_id)
    reservations = ReservationController.get_by_projection_id(projection.id)
    taken_spots = {(r.row, r.col) for r in reservations}

    available_spots = ROWS * COLS - len(taken_spots)
    new_reservations = []

    if tickets > available_spots:
        print('Error: there are not that many available spots')
        return

    print_theater(taken_spots)

    new_reservations = []
    i = 0
    while i < tickets:
        position = map(int, input(f'Choose seat {i+1}> ').strip('() ').split(','))
        position = tuple(position)
        if position in taken_spots:
            print('Lel... Nope')
            continue

        new_reservations.append(Reservation(projection_id=projection_id, row=position[0], col=position[1]))
        i += 1

    UserController.make_reservations(username, new_reservations)


def print_theater(taken_spots):
    theater = [deepcopy(['.'] * COLS) for _ in range(ROWS)]

    for spot in taken_spots:
        theater[spot[0]-1][spot[1]-1] = 'X'

    print('  ', ' '.join(map(str, range(1, ROWS+1))))
    for i, row in zip(range(ROWS), theater):
        print(str(i+1).ljust(2), ' '.join(row))
