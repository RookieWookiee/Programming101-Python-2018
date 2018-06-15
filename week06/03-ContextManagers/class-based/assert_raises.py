class assertRaises:
    def __init__(self, *exc_types, **kwargs):
        if any(not issubclass(x, BaseException) for x in exc_types):
            raise TypeError('postional arguments must be derived from BaseException')

        self.exc_types = exc_types
        self.msg = kwargs.get('msg')
    
    def __enter__(self):
        pass

    def __exit__(self, e_type, e_val, e_tback):
        if any(e_type == x for x in self.exc_types):
            if self.msg == None:
                return True

            if self.msg != str(e_val):
                print(f"Messages differ: expected '{self.msg}', got '{str(e_val)}")
            return self.msg == str(e_val)

        print(f'None of the {self.exc_types} was raised')
        return False


if __name__ == '__main__':
    with assertRaises(ValueError, TypeError, StopIteration, msg='do mind me'):
        raise StopIteration("do mind me")
