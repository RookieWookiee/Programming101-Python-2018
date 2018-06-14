import json
import collections
from jsonable import JsonableMixin as Jsonable


class Xmlable:
    def to_xml(self, indent=4):
        pass

    @classmethod
    def from_xml(cls, xml_string):
        pass


class Test3(Jsonable):
    def __init__(self, foo):
        self.foo = 'test3'


class Test2(Jsonable):
    def __init__(self, foo, bar):
        self.foo = 'test2'
        self.bar = Test3(None)


class Test(Jsonable, Xmlable):
    def __init__(self, foo, bar, baZ, baz):
        self.foo = 42
        self.bar = [1, 2, 3, 4]
        self.baZ = [Test3(None), Test3(None)]
        self.baz = Test2(*([None] * 2))

    def foo_method(self):
        pass


if __name__ == '__main__':
    t = Test(None, None, None, None)
    json_ = t.to_json()
    print(t.to_json())
    t2 = Test.from_json(t.to_json(), globals())
    print(t2.to_json() == t.to_json())

