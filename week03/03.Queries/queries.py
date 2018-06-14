import csv


def get_fields(fname):
    res = fname.readline().split(',')
    return list(filter(None, res))


def bind_fields_to_indeces(fields):
    return {x: i for i, x in enumerate(fields)}


def gen_valid_kwargs(d):
    suffixes = ['__startswith', '__gt', '__lt', '__contains']
    args = set(d.keys())
    suffixed_args = set(f'{key}{suffix}' for key in d for suffix in suffixes)

    return args.union(suffixed_args)


def gen_filters(fields_lookup, **kwargs):
    filters = []
    for arg in kwargs:
        if arg == 'order_by':
            continue

        elif arg.endswith('__gt'):
            key = arg[:-len('__gt')]
            field_i, target = fields_lookup[key], kwargs[arg]

            filters.append((lambda i, t: lambda tokens: int(tokens[i]) > t)(field_i, target))

        elif arg.endswith('__lt'):
            key = arg[:-len('__lt')]
            field_i, target = fields_lookup[key], kwargs[arg]

            filters.append((lambda i, t: lambda tokens: int(tokens[i]) < t)(field_i, target))

        elif arg.endswith('__contains'):
            key = arg[:-len('__contains')]
            field_i, target = fields_lookup[key], kwargs[arg]

            filters.append((lambda i, t: lambda tokens: t in tokens[i])(field_i, target))

        elif arg.endswith('__startswith'):
            key = arg[:-len('__startswith')]
            field_i, target = fields_lookup[key], kwargs[arg]

            filters.append((lambda i, t: lambda tokens: tokens[i].startswith(t))(field_i, target))

        else:
            field_i, target = fields_lookup[arg], kwargs[arg]

            filters.append((lambda i, t: lambda tokens: tokens[i] == t)(field_i, target))

    return filters


def apply_filters(filters, tokens):
    return all(f(tokens) for f in filters)


def order_by(l, field_i):
    try:
        l.sort(key=lambda x: int(x[field_i]))
    except:
        l.sort(key=lambda x: x[field_i])


def csv_filter(fname, **kwargs):
    with open(fname, newline='') as csvf:
        reader = csv.reader(csvf)

        fields = next(reader)
        fields_lookup = bind_fields_to_indeces(fields)
        valid_args = gen_valid_kwargs(fields_lookup)

        if any(x not in valid_args and x != 'order_by' for x in kwargs):
            raise TypeError('Invalid keyword argument')

        filters = gen_filters(fields_lookup, **kwargs)
        result = [x for x in reader if all(f(x) for f in filters)]

        if 'order_by' in kwargs:
            criteria = kwargs['order_by']
            field = fields_lookup[criteria]
            order_by(result, field)

        return result


def csv_count(fname, **kwargs):
    return len(csv_filter(fname, **kwargs))


def csv_first(fname, **kwargs):
    if('order_by' not in kwargs):
        with open(fname, newline='') as csvf:
            reader = csv.reader(csvf)

            fields = next(reader)
            fields_lookup = bind_fields_to_indeces(fields)
            valid_args = gen_valid_kwargs(fields_lookup)

            if any(x not in valid_args and x != 'order_by' for x in kwargs):
                raise TypeError('Invalid keyword argument')

            filters = gen_filters(fields_lookup, **kwargs)

            return next(x for x in reader if all(f(x) for f in filters))
    else:
        return csv_filter(fname, **kwargs)[0]


def csv_last(fname, **kwargs):
    if('order_by' not in kwargs):
        with open(fname, newline='') as csvf:
            reader = csv.reader(csvf)

            fields = next(reader)
            fields_lookup = bind_fields_to_indeces(fields)
            valid_args = gen_valid_kwargs(fields_lookup)

            if any(x not in valid_args and x != 'order_by' for x in kwargs):
                raise TypeError('Invalid keyword argument')

            filters = gen_filters(fields_lookup, **kwargs)

            return next(x for x in reader if all(f(x) for f in filters))
    else:
        return csv_filter(fname, **kwargs)[-1]
