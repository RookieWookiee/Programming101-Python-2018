class Controller:
    @classmethod
    def create_user(cls, *params):
        return User.create(*params)


------------------------------------
class User:
    user_proxy = UserProxy()
    user_validator = UserValidator()
    @classmethod
    def create(cls, *params):
        cls.user_validator.validate_user_creation()
        # hash password
        cls.user_proxy.create(params)
        return cls()

--------------------------------
class UserProxy:
    db_conn = ...
    @classmethod
    def create(cls, *params):
        db_conn.execute(UserQueryConstant.INSERT_NEW_USER, params)
