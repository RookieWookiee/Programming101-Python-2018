# Tasks

Every dictionary in the following tasks can have another dictionary as value or a iterable of dictionaries.

## Task 1

Implement `deep_find(data, key)` which finds the given `key` in the `data` and returns it's value.

## Task 2

Implement `deep_find_all(data, key)` which finds the given `key` in the `data` and returns array of the found values.

## Task 3

Implement `deep_update(data, key, val)` which updates every occurance of the given `key` in the `data` with `val`.

## Task 4

Implement `deep_apply(func, data)` which applies the given `func` to all **keys** from the given `data`.

## Task 5

Implement `deep_compare(obj1, obj2)` where obj1 and obj2 can be `dict` or `iterable` and compares the given objects.

## Task 6

Implement `schema_validator(schema: List, data: Dict)` which should assert that the given `data` keys are as the given `schema`.
**Notes**
* `data` is valid only if the given keys from the `schema` are found in the `data`.
* If the `schema` has more or less keys, `data` is invalid.
* If there is a missmatch in the `schema` and the `data` keys, `data` is invalid.
* `schema_validator` should work for N levels of nesting.

Example `schema`:

```
schema = [
    'key1',
    'key2',
    [
        'key3',
        ['inner_key1', 'inner_key2']
    ]
]
```

Valid `data`:

```
data = {
    'key1': 'val1',
    'key2': 'val2',
    'key3': {
        'inner_key1': 'val1',
        'inner_key2': 'val2'
    }
}
```

Invalid `data`:

```
data = {
    'key1': 'val1',
    'key2': 'val2',
    'key3': {
        'inner_key1': 'val1',
        'inner_key2': 'val2'
    },
    'key4': 'not expected'
}
```