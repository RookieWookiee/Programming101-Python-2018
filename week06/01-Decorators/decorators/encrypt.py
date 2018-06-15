from functools import wraps


def encrypt(ceasar_offset):
    def accepter(func):
        @wraps(func)
        def decorator(*args):
            res = func(*args)

            dec = []
            for x in res:
                if x.islower():
                    dec.append(chr(((ord(x) - ord('a') + ceasar_offset) % 26) + ord('a')))
                elif x.isupper():
                    dec.append(chr(((ord(x) - ord('A') + ceasar_offset) % 26) + ord('A')))
                else:
                    dec.append(x)

            return ''.join(dec)
        return decorator
    return accepter
