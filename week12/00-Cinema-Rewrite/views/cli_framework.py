''' Poor Man's Click -
    Collection of functions for easier building of command line tools.
    Basic clone of the click framework.
'''


from enum import IntEnum
from contextlib import wraps
from collections import Iterable, deque, OrderedDict


import six
import readline
import logging
import os


LOG_FNAME = '/tmp/completer.log'
LOG_LEVEL = logging.DEBUG
logging.basicConfig(filename=LOG_FNAME, level=LOG_LEVEL)


# *silent contempt* TODO: refactor this oopsie woosie dookie wookie fucko boingo
command_tree = {}
command_aliases = {}
help_lookup = {}
command_to_func_lookup = {}
cli_entry_point = None
func_arguments = {}
func_flags = {}

env = {}


class BadArgument(Exception):
    '''Basic wrapper for when validation function has failed.'''
    pass


class CommandNotFoundError(Exception):
    def __init__(self, message, command_name):
        super().__init__(message)
        self.command_name = command_name


class Type(IntEnum):
    COMMAND = 1
    GROUP = 2


def _dealiasify(func):
    """Decorator for dealisifying command name arguments.

       Example: if 'h' is alias for 'help' and 'q' is for 'quit':
         _dealisify(func)('h', *args) will result in func('help', *args)
         _dealisify(func)('help') will result in func('help')
         _dealisify(func)(['h', 'q']) will result in func(['help', 'quit'])
    """

    @wraps(func)
    def decorated(tokens, *args, **kwargs):
        if isinstance(tokens, Iterable):
            if all(not isinstance(tokens, s_type) for s_type in six.string_types):
                actual_cmd = [command_aliases[x] if x in command_aliases else x
                              for x in tokens]
        else:
            actual_cmd = (command_aliases[tokens]
                          if tokens in command_aliases
                          else tokens)

        return func(actual_cmd, *args, **kwargs)
    return decorated


@_dealiasify
def find_command(needle, node=None):
    """ returns the functions associated with the 'needle'

        :param needle: str or Iterable of strings
        :param node - dict: optional starting point for the search
        :return: A tuple with:
             [0] - the wrapped function object,
             [1] - a dict with its' subcommands,
             [2] - the rest of the arguments for command to be called with
        :raises CommandNotFoundError:"""

    if node is None:
        node = cli_entry_point
    if isinstance(needle, Iterable) and type(needle) is not str:
        # find([<full>, <path>, <to>, <subcommand>])
        if needle[0] not in node:
            raise CommandNotFoundError(
                f"Error: Command '{needle[0]}' not found", needle[0]
            )

        curr_cmd, curr_cmd_dict = node[needle[0]]
        if len(needle) == 1:
            wrapper, wrapped_dict = node[needle[0]]
            return wrapper, wrapped_dict, None
        elif node[needle[0]][0].type is Type.COMMAND:
            wrapper, wrapped_dict = node[needle[0]]
            return wrapper, wrapped_dict, needle[1:]

        return find_command(needle[1:], node[needle[0]][1])
    else:
        # find(<subcommand>)
        q = deque()
        q.append(node)

        while len(q) != 0:
            curr = q.popleft()
            if needle in curr:
                return curr[needle]
            for k in curr:
                q.append(curr[k][1])

        raise CommandNotFoundError(
            f"Error: Command '{needle}' not found", needle[0]
        )


# test_dict = {
#     # Instead of lambdas there'll be WrappedCommands
#     'show': (lambda: print('show'), {
#         'movie': (lambda: print('show movie'), {
#             'projections': (lambda: print('show movie projections'), {}),
#         }),
#         'movies': (lambda: print('show movies'), {}),
#     }),
#     'make': (lambda: print('make'), {
#         'reservation': (lambda: print('make reservation'), {}),
#     }),
#     'help': (lambda: print('help'), {})
# }
#
# command_aliases['proj'] = 'projections'
# try:
#     func, func_dict = find_command(['show', 'movie', 'proj'], test_dict)
#     func()
# except CommandNotFoundError as e:
#     print(e)


class CommandWrapper:
    def __init__(self, func, cmd_name):
        self.func = func
        self.command_name = cmd_name
        self.command_tree = {}
        self.parent_command = None
        self.help_lookup = {}

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def group(self, *args, **kwargs):
        def accepter(command_func):
            return self._wrap(command_func, Type.GROUP, *args, **kwargs)
        return accepter

    def command(self, *args, **kwargs):
        def accepter(command_func):
            return self._wrap(command_func, Type.COMMAND, *args, **kwargs)
        return accepter

    def _wrap(self, func, func_type, *args, **kwargs):
        """ Wraps func within a class with group and command functions
            of its own.

            :param func: the function to be wrapped
            :param func_type: Type.COMMAND or Type.GROUP
            :param args: if one positional argument is supplied,
                    it will be used as the identifier for the command
            :param kwargs: 
                    optional kwargs - 
                    'help' - the help string for when 'help' is invoked,
                            if it's not supplied the doc string would be used
                    'aliases' - additional identifiers to be bound to the command
        """
        cmd_name = args[0] if len(args) > 0 else func.__name__

        for alias in kwargs.get('aliases', []):
            command_aliases[alias] = cmd_name

        help_str = kwargs.get('help', func.__doc__)
        self.help_lookup[func.__name__] = help_str
        help_lookup[func.__name__] = help_str

        wrapped = CommandWrapper(func, cmd_name)
        wrapped.parent = self
        wrapped.type = func_type

        func_dict = {k: getattr(func, k) for k in dir(func)}
        missing_keys = set(func_dict) - set(dir(wrapped)) 
        func_meta_info = {k: getattr(func, k) for k in missing_keys if k != '__globals__'}
        wrapped.__dict__.update(func_meta_info)

        self.command_tree[cmd_name] = (wrapped, wrapped.command_tree)

        command_to_func_lookup[cmd_name] = func.__name__

        return wrapped

    def validate_args(self, actual_args):
        if actual_args is None:
            actual_args = []

        func_name = self.__name__
        formal_args = func_arguments.get(func_name, {})

        if len(actual_args) < len(formal_args):
            raise ValueError

        actual_kwargs = {}
        actual_args_iter = iter(actual_args)
        formal_args_iter = iter(formal_args)

        for arg in actual_args_iter:
            # Treat as flag
            if arg.startswith('-') and len(arg) > 1:
                flag, validator = arg, func_flags\
                    .get(func_name)\
                    .get(arg)['validator']
                validator_args = []
                for _ in range(validator.__code__.co_argcount):
                    validator_args.append(next(actual_args_iter))

                actual_kwargs[flag] = validator(*validator_args)
            elif arg == '-':
                # TODO:
                # skip it and start treating everything that follows literally
                # (as is)
                pass
            # argument
            else:
                try:
                    formal_arg = next(formal_args_iter)
                    validator = formal_args[formal_arg].get('validator')
                except StopIteration:
                    # Hacky variadic arguments
                    if type(actual_kwargs[formal_arg]) is not list:
                        actual_kwargs[formal_arg] = [actual_kwargs[formal_arg]]

                    actual_kwargs[formal_arg].extend([validator(arg)])
                else:
                    actual_kwargs[formal_arg] = validator(arg)

        # get default values for missing flags
        for flag in set(func_flags.get(func_name, [])) - set(actual_kwargs):
            validator = func_flags[func_name][flag]['validator']
            actual_kwargs[flag] = validator(
                *([None] * validator.__code__.co_argcount)
            )

        return {k.strip('-'): v for k, v in actual_kwargs.items()}


def _no_validation(arg):
    return arg


def argument(*args, **kwargs):
    assert len(args) > 0

    def accepter(func):
        arg_name = args[0]

        fname = func.__name__

        if fname not in func_arguments:
            func_arguments[fname] = OrderedDict()
            func_arguments[fname][arg_name] = {}


        validator = kwargs.get('callback')
        validator = validator if validator is not None else kwargs.get('type')
        validator = validator if validator is not None else _no_validation

        func_arguments[fname][arg_name]['validator'] = validator

        if 'help' in kwargs:
            func_arguments[fname][arg_name]['help'] = kwargs['help']

        return func
    return accepter


def flag(*args, **kwargs):
    assert len(args) > 0

    def accepter(func):
        flag_name = args[0]

        fname = func.__name__

        if fname not in func_flags:
            func_flags[fname] = {}

        validator = kwargs.get('callback')
        validator = validator if validator is not None else kwargs.get('type')
        validator = validator if validator is not None else _no_validation

        final_validator = None
        if 'default' in kwargs:
            final_validator = lambda x: (kwargs.get('default')
                                         if x is None
                                         else validator(x))
        else:
            final_validator = validator
        
        if flag_name not in func_flags[fname]:
            func_flags[fname][flag_name] = {}

        func_flags[fname][flag_name]['validator'] = final_validator

        if 'help' in kwargs:
            func_flags[fname][flag_name]['help'] = kwargs.get('help')

        return func
    return accepter


def pass_env(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        func(env=env, *args, **kwargs)
    return decorated


def entry_point(*dec_args, **dec_kwargs):
    def accepter(func):
        global cli_entry_point

        wrapped = CommandWrapper(func, func.__name__)
        wrapped.parent_command = None
        cli_entry_point = wrapped.command_tree

        return wrapped
    return accepter


def start_repl(prompt='> '):
    while True:
        try:
            user_input = list(filter(None, input(prompt).split()))
        except EOFError:
            print()
            return
        if user_input == []:
            continue

        try:
            command, _, actual_args = find_command(user_input)
        except CommandNotFoundError as e:
            print(e)
            continue

        try:
            cmd_kwargs = command.validate_args(actual_args)
            command(**cmd_kwargs)
        except BadArgument as e:
            print(e)


files = [
    'views.commands.cli',
    'views.commands.show.show',
    'views.commands.make.make',
    'views.commands.cancel.cancel',
]

for f in files:
    __import__(f)

readline.parse_and_bind('tab: complete')


class SimpleCompleter:
    def __init__(self):
        self.options = self.__get_command_tree()
        print()

    def __get_command_tree(self, node=None, res=None):
        res = {}
        if node is None:
            node = cli_entry_point

        for k, v in node.items():
            res[k] = self.__get_command_tree(v[1], res)
        return res

    def complete(self, text, state):
        tokens = list(filter(None, text.split()))
        tokens.append('')
        i = 0
        current = cli_entry_point

        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                while True:
                    if i >= len(tokens):
                        break
                    curr_word = tokens[i]
                    if curr_word not in current:
                        break
                    current = current[curr_word][1]
                    i += 1

                self.matches = [s
                                for s in current
                                if s and s.startswith(tokens[i])]
                logging.debug(f'{repr(text)} matches: {self.matches}')
            else:
                self.matches = list(current.keys())[:]
                logging.debug(f'(empty input) matches: {self.matches}')

        try:
            response = self.matches[state]
            response = (' '.join(tokens[:i]) + ' ' + response).strip()
        except IndexError:
            response = None
            logging.debug(f'complete("{text}", {state}) -> {response}')

        return response


readline.set_completer_delims(os.linesep)
readline.set_completer(SimpleCompleter().complete)
# Use the tab key for completion
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')
