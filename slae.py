def swap_lines(matrix, first, second, width):
    for j in range(width):
        matrix[first][j], matrix[second][j] = matrix[second][j], matrix[first][j]


def mul_line(matrix, w, line, alpha):
    for j in range(w):
        matrix[line][j] *= alpha


def sub_lines(matrix, w, left, right,  k=1):
    for j in range(w):
        matrix[left][j] -= matrix[right][j]*k


def gcd(a, b):
    assert a*b != 0
    a = abs(a)
    b = abs(b)
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a


def transform(matrix, h, w):
    """
    :param matrix: matrix h*w (inplace transforming)
    :param h:
    :param w:
    :return: None
    """
    for j in range(min(w, h)):
        i = j
        while (i < h) and matrix[i][j] == 0:
            i += 1
        if (i != j) and (i != h):
            swap_lines(matrix, i, j, width=w)
        if matrix[j][j] < 0:
            mul_line(matrix, w, j, -1)
        for i in range(j + 1, h):
            if matrix[i][j] == 0:
                continue
            mul_line(matrix, w, i, matrix[j][j] // gcd(matrix[j][j], matrix[i][j]))
            sub_lines(matrix, w, i, j, matrix[i][j] // gcd(matrix[j][j], matrix[i][j]))


def solve_determined(matrix, h, w):
    """
    :param matrix: square matrix with non zero determinant
    :param h:
    :param w:
    :return:
    """
    ans_list = [0]*(w-1)
    for j in range(w-2, 0-1, -1):
        sm = sum(matrix[j][i]*ans_list[i] for i in range(0, w-1))
        x_j = (matrix[j][w-1] - sm) / matrix[j][j]
        ans_list[j] = x_j
    return ans_list


def extend_matrix(matrix, h, w, vector):
    """
    :param matrix: matrix h*w
    :param h:
    :param w:
    :param vector: vector of h elements
    :return: matrix h*(w+1)
    """
    res = [matrix[i].copy() for i in range(h)]
    for i in range(h):
        res[i].append(vector[i])
    return res


def partial_solution(equation: list[list], h: int, w: int) -> list:
    """
    Getting partial solution of system of linear equations
    :param equation: matrix h*w
    :param h:
    :param w:
    """
    matrix = [line.copy() for line in equation]
    transform(matrix, h, w)
    base_columns = []
    j = 0
    for i in range(h):
        while (j < w - 1) and (matrix[i][j] == 0):
            j += 1
        if j == w - 1:
            break
        base_columns.append(j)
    # print(f"{base_columns=}")

    n = len(base_columns)

    assert all(matrix[i][w-1] == 0 for i in range(n, h)), "No solutions"

    new_matrix = [[0] * n for _ in range(n)]

    for j_pos, j in enumerate(base_columns):
        for i in range(n):
            new_matrix[i][j_pos] = matrix[i][j]

    new_matrix = extend_matrix(new_matrix, n, n, [matrix[i][w-1] for i in range(n)])

    solution = solve_determined(new_matrix, n, n+1)
    res = [0] * (w-1)
    for j_pos, j in enumerate(base_columns):
        res[j] = solution[j_pos]
    return res
