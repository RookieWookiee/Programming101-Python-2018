import json
import collections

"""
I think if I add a couple of more lines, the code will become sentient.
Please refactor.
"""

class JsonableMixin:
    def _serialize_dict(self, _dict, **kwargs):
        _json = {}
        for k, v in _dict.items():
            if k in kwargs:
                pairs = kwargs[k](self, v)
                for new_k, new_v in pairs:
                    _json[new_k] = new_v
            elif k in kwargs.get('ignore', []) or k.startswith('_'):
                continue
            elif isinstance(v, JsonableMixin):
                _json[k] = v.to_dict()
            elif isinstance(v, dict):
                _json[k] = self._serialize_dict(v, **kwargs)
            elif isinstance(v, collections.Iterable) and not isinstance(v, str):
                _json[k] = self._serialize_list(v, **kwargs)
            else:
                _json[k] = v

        return _json

    def _serialize_list(self, collection, **kwargs):
        _json = []
        for v in collection:
            if isinstance(v, JsonableMixin):
                _json.append(v.to_dict())
            elif isinstance(v, dict):
                _json.append(self._serialize_dict(v, **kwargs))
            elif isinstance(v, collections.Iterable) and not isinstance(v, str):
                _json.append(JsonableMixin._serialize_list(v))
            else:
                _json.append(v)

        return _json

    def to_dict(self, **kwargs):
        _json = self._serialize_dict(self.__dict__, **kwargs)
        return {'class_name': self.__class__.__name__, 'dict': _json}

    def to_json(self, **kwargs):
        _json = self._serialize_dict(self.__dict__, **kwargs)
        return json.dumps({'class_name': self.__class__.__name__, 'dict': _json}, indent=4)

    @staticmethod
    def _deserialize_collection(seq, namespace):
        res = []
        for el in seq:
            if isinstance(el, dict):
                if el.get('class_name') is not None:
                    if namespace.get(el['class_name']) is None:
                        raise ValueError(f'There is no {el["classname"]} class identifier in the current namespace')
                    else:
                        res.append(namespace.get(el['class_name']).from_json(el, namespace))
            else:
                res.append(el)
        return res

    @classmethod
    def from_json(cls, dict_, namespace, **kwargs):
        # (future me) - *desire for eye-gauging intensifies*
        if type(dict_) is str:
            dict_ = json.loads(dict_)

        if dict_.get('class_name') is None or dict_.get('class_name') != cls.__name__:
            raise ValueError('JSON in incorrect format')
        if dict_['class_name'] != cls.__name__:
            raise ValueError(f'There is no {dict_["class_name"]} class identifier in the current namespace')

        class_name = dict_['class_name']
        ctor_args = {}

        for k, v in dict_['dict'].items():
            if k in kwargs.get('ctor_ignore', []):
                continue

            if isinstance(v, dict):
                if v.get('class_name') is not None:
                    if namespace.get(v['class_name']) is None:
                        raise ValueError(f'There is no {k["class_name"]} class identifier in the current namespace')
                    else:
                        ctor_args[k] = namespace.get(v['class_name']).from_json(v, namespace)

            elif isinstance(v, collections.Iterable) and not isinstance(v, str):
                ctor_args[k] = cls._deserialize_collection(v, namespace)
            else:
                ctor_args[k] = v

        obj = cls(**ctor_args)

        post_ctor = kwargs.get('post_ctor', {})
        for key, f in post_ctor.items():
            f(obj, dict_['dict'].get(key))

        return obj
