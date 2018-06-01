from pprint import pprint


class Attr:
    def __init__(self, attr_type):
        self.attr_type = attr_type

    def __call__(self, value):
        return type(value) is self.attr_type

    def __str__(self):
        return str(self.attr_type)

    def __repr__(self):
        return str(self)


class declarative_meta(type):
    def __new__(cls, name, bases, clsdict):
        attributes = {}

        for base in bases:
            attributes.update(vars(base)['_attributes'])

        attributes.update({
            attr_name: attr_value
            for attr_name, attr_value in clsdict.items()
            if isinstance(attr_value, Attr)
        })

        clsdict['_attributes'] = attributes

        clsobj = super().__new__(cls, name, bases, clsdict)

        return clsobj


class Base(metaclass=declarative_meta):
    def __init__(self, **kwargs):
        attributes = getattr(self, '_attributes', [])

        for attr, attr_value in kwargs.items():
            if attr not in attributes:
                raise TypeError(f'{attr} not in {attributes}')

            attr_type = attributes[attr]

            if not attr_type(attr_value):
                raise TypeError(f'{attr} is not a valid type. Expected {attr_type}')

            setattr(self, attr, attr_value)


class Foo(Base):
    a = Attr(int)
    b = Attr(str)
    c = Attr(int)


class A(Foo):
    a = Attr(str)

A(a='1')
print(A._attributes)
