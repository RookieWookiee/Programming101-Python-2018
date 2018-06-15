from bfs import bfs


def deep_find(data, needle):
    def find_first(data, k, v, match=None, needle=needle):
        if match is None and k == needle:
            match = v

        return match

    return bfs(data, find_first)


d = {
    0: [
        {2: 'g'},
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

print('deep find', deep_find(d, 2))
