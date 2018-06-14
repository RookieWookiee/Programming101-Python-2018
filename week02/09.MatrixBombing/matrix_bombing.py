from copy import deepcopy


# Problem05
def matrix_bombing_plan(m):
    def bomb(i, m):
        matrix = deepcopy(m)
        y = i // len(matrix)
        x = i % len(matrix[y])
        power = matrix[y][x]

        def in_bounds_row(r): return r >= 0 and r < len(matrix)

        def in_bounds_col(c): return c >= 0 and c < len(matrix[y])

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if(dy == 0 and dx == 0):
                    continue
                if in_bounds_row(y+dy) and in_bounds_col(x+dx):
                    matrix[y+dy][x+dx] = max(0, matrix[y+dy][x+dx]-power)

        _sum = sum(x for row in matrix for x in row)
        return ((y, x), _sum)

    flatten = [x for row in m for x in row]
    bombed = {t[0]: t[1] for t in {bomb(i, m) for i in range(len(flatten))}}
    return bombed
