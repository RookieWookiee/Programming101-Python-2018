from bfs import bfs


def deep_find_all(data, needle):
    def find_all(data, k, v, acc=None, needle=needle):
        if acc is None:
            acc = []
        if k == needle:
            acc.append(v)
        return acc

    return bfs(data, find_all)


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

print('deep find all', deep_find_all(d, 2))
