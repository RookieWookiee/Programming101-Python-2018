from views.cli_framework import entry_point, CommandNotFoundError
from views import cli_framework
from utils.decorators import interruptable
from tabulate import tabulate

from controllers.user_controller import UserController

import sys
import os
import getpass


@entry_point()
def cli():
    pass


@cli.group()
def show():
    '''show help doc string'''
    pass


@cli.command(aliases=['exit', 'q'])
def quit():
    '''stops the program'''
    sys.exit(0)


@cli.group()
def make():
    '''make help doc string'''
    pass


@cli.group()
def cancel():
    '''cancel help doc string'''
    pass


@cli.command()
@cli_framework.pass_env
def logout(env):
    '''logs out the user'''
    env['user'] = None


# TODO: remember successful authentications for a set period of time
#       like sudo
@cli.command()
@cli_framework.flag('--username', default=None,
                    help='Username to be used for login')
@cli_framework.flag('--password', default=None,
                    help='Password to be used for login')
@interruptable
@cli_framework.pass_env
def login(env, username, password):
    '''login doc string'''
    # TODO: save user login in the env variables
    ppid = os.getppid()

    if username is None:
        username = input('Username: ')

    if not UserController.exists(username=username):
        print('No such user, register first')
        return

    if password is None:
        password = getpass.getpass()

    if not UserController.check_password(username, password):
        print('Error: Incorrect password')
        return

    env['user'] = username


@cli.command()
@cli_framework.flag('--username', default=None)
@cli_framework.flag('--password', default=None)
@interruptable
def register(username, password):
    '''register doc string'''
    if password is not None:
        if not UserController.validate_password(password):
            print('password does not conform to the standard')
            print('please contact your local arch bishop')
            return

    confirm_passwd = password is None
    if username is None:
        username = input('Username: ')

    if UserController.exists(username=username):
        print('Error: Username already exists')
        return

    if password is None:
        password = getpass.getpass()

    if not UserController.validate_password(password):
        print('Error: password does not conform to the standard')
        print('Please contact your local arch bishop.')
        return

    if confirm_passwd:
        confirmation = getpass.getpass('Confirm password:')

        if password != confirmation:
            print('Passwords do not match')
            return

    UserController.register(username, password)


@cli.command()
def clear():
    '''Clears the screen'''
    os.system('cls' if os.name == 'nt' else 'clear')


@cli.command(aliases=['h'])
@cli_framework.argument('command', help='Target command')
def help(command):
    ''' print this help message '''
    try:
        cmd = cli_framework.find_command(command)
    except CommandNotFoundError as e:
        print(e)
        return

    func = cmd[0].func
    sub_commands = cmd[1]

    usage = f'Usage: {" ".join(command) if type(command) is list else command}'
    args = cli_framework.func_arguments.get(func.__name__)
    flags = cli_framework.func_flags.get(func.__name__)

    if flags is not None:
        usage += f' [OPTIONS]'

    if args is not None:
        usage += ' ' + ' '.join(x.upper() for x in args)

    print(usage)

    if cli_framework.help_lookup.get(func.__name__) is not None:
        print(os.linesep, cli_framework.help_lookup.get(func.__name__))

    if flags is not None:
        print()
        print('Options:')
        flags_help = [cli_framework.func_flags
                .get(func.__name__, {})
                .get(flag, {})
                .get('help', ' ')
                for flag in flags]

        print(os.linesep.join(f'{flag.ljust(15)} {help_str}'for flag, help_str in zip(flags, flags_help)))

    if args is not None:
        print()
        print('Arguments:')
        args_help = [cli_framework.func_arguments
                .get(func.__name__, {})
                .get(arg, {})
                .get('help', ' ')
                for arg in args]
        print(os.linesep.join(f'{arg.upper().ljust(15)} {help_str}'for arg, help_str in zip(args, args_help)))

    print()


@cli.command()
@cli_framework.pass_env
def whoami(env):
    '''Print the username of the user if logged.'''
    print(env.get('user'))
