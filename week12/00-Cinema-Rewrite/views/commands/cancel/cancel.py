from views.commands.cli import cancel
from views import cli_framework
from controllers.user_controller import UserController, user_exists


@cancel.command('reservation')
@cli_framework.argument('username')
@user_exists
def cancel_reservation(username):
    UserController.delete_reservations(username)
