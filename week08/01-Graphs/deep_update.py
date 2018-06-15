from bfs import bfs


def deep_update(data, key, val):
    def update(data, k, v, acc, needle=key, val=val):
        if k == needle:
            data[k] = val

    bfs(data, update)


d = {
    0: [
        {2: 'gm'},
    ],
    1: 'a',
    2: 'b',
    3: {
        2: 'c',
        3: 'd',
        4: {
            2: 'd',
        },
    },
}

deep_update(d, 2, 'z')
print('deep update', d)
