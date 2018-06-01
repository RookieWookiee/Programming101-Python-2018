from datetime import datetime

from serializers import Serializer
from fields import CharField, EmailField, DateTimeField


class Panda:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.now()


class PandaSerializer(Serializer):
    name = CharField()
    email = EmailField()
    created_at = DateTimeField()

def main():
    p = Panda('Ivo', 'ivo@hackbulgaria.com')
    s = PandaSerializer(instance=p)

    import ipdb; ipdb.set_trace()

    print('asdsadas')


if __name__ == '__main__':
    main()
