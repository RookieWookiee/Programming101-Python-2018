from collections import deque, Iterable


def bfs(data, action):
    q = deque()
    q.append(data)
    thing = None

    while q:
        curr = q.pop()

        if isinstance(curr, dict):
            for k, v in curr.items():
                thing = action(curr, k, v, thing)
                q.append(v)
        elif (isinstance(curr, Iterable)
                and type(curr) is not str):
            for v in curr:
                q.append(v)

    return thing
