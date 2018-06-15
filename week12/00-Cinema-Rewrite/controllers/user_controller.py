from db_layer.session import Session, engine
from models.user import Reservation, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import delete
from contextlib import wraps, closing

import hashlib
import uuid


def user_exists(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        username = kwargs['username'] if 'username' in kwargs else args[0]
        if not UserController.exists(username):
            print('Error: username does not exist')
            return

        func(*args, **kwargs)
    return decorated


def user_logged_in(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        env = kwargs.get('env', {})
        if env.get('user') is None:
            print('Error: you must be logged in')
            return

        kwargs['username'] = env.get('user')

        new_kwargs = {k: v for k, v in kwargs.items() if k != 'env'}
        func(*args, **new_kwargs)
    return decorated


class ReservationController:
    ROWS = 10
    COLS = 10

    @classmethod
    def get_by_projection_id(cls, id):
        session = Session()
        return session.query(Reservation).filter(Reservation.projection_id == id).all()

    def delete_by(**kwargs):
        if len(kwargs) != 1:
            raise ValueError(f'Expected 1 argument, got {len(kwargs)}')

        by = next(iter(kwargs))
        if not hasattr(Reservation, by):
            raise ValueError(f'Reservation has not {by} attribute')


        stmt = delete(Reservation).where(getattr(Reservation, by) == kwargs[by])
        with closing(engine.connect()) as conn:
            conn.execute(stmt)


class UserController:
    def get_by(**kwargs):
        if len(kwargs) != 1:
            raise ValueError(f'Expected 1 argument, got {len(kwargs)}')

        by = next(iter(kwargs))
        if not hasattr(User, by):
            raise ValueError(f'User has not {by} attribute')

        session = Session()

        response = session.query(User).filter(getattr(User, by) == kwargs[by]).all()
        return response[0] if len(response) == 1 else response

    @classmethod
    def exists(cls, username):
        session = Session()

        try:
            session.query(User).filter(User.username == username).one()
            return True
        except NoResultFound:
            return False

    @classmethod
    def validate_password(cls, password):
        return (
            len(password) >= 8 and
            any(x.isupper() for x in password) and
            any(not x.isalnum() for x in password)
        )

    @classmethod
    def register(cls, username, password):
        password, salt = cls.hash_password(password)
        user = User(username=username, password=password, salt=salt)
        session = Session()
        session.add(user)
        session.commit()

    @classmethod
    def check_password(cls, username, password):
        session = Session()
        user = cls.get_by(username=username)
        
        _hash = hashlib.sha256(user.salt.encode() + password.encode()).hexdigest()
        return _hash == user.password

    @classmethod
    def hash_password(cls, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt

    @classmethod
    def make_reservations(cls, username, new_reservations):
        session = Session()

        user = session.query(User).filter(User.username == username).one()
        user.reservations.extend(new_reservations)

        session.add(user)
        session.commit()

    @classmethod
    def delete_reservations(cls, username):
        uid = cls.get_by(username=username).id
        ReservationController.delete_by(user_id=uid)
