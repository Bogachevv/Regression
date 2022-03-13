import random
from slae import extend_matrix, partial_solution
from vectors import *
from vec_exceptions import SizeMismatch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def print_matrix(matrix, h, w):
    for i in range(h):
        for j in range(w):
            print(matrix[i][j], end=" ")
        print()


def test(equation, right, solution):
    x_vec = solution.copy()
    solution_right = matrix_vector_permutation(equation, solution, len(solution), len(equation))
    print(f"{solution_right=}")
    delta = sub_vectors(solution_right, right)
    delta = np.sqrt(scalar_permutation(delta, delta))
    print(f"Solution {delta=}")
    for x in np.linspace(5, 15, 1000):
        x_vec[0] = x
        x_right = matrix_vector_permutation(equation, x_vec, len(x_vec), len(equation))
        x_delta = sub_vectors(x_right, right)
        x_delta = np.sqrt(scalar_permutation(x_delta, x_delta))
        # print(f"{delta=}, {x_delta=}")
        if x_delta < delta:
            print(f"{x=}, {delta=}, {x_delta=}")


def solve(*vector_list, right):
    vectors = [vec.copy() for vec in vector_list]
    m = len(vectors)
    n = len(vectors[0])
    vectors = [[vectors[i][j] for i in range(m)] for j in range(n)]
    gram = build_gram(*vectors)
    equation = extend_matrix(gram, n, n, [scalar_permutation(vec, right) for vec in vectors])
    solution = partial_solution(equation, n, n + 1)
    return solution


def main():
    n = int(input("Input variables count: "))
    m = int(input("Input equations count: "))

    vectors = [list(map(int, input(f"a[{i}] = ").strip().split())) for i in range(m)]

    old_vectors = [[vectors[i][j] for j in range(n)] for i in range(m)]

    vectors = [[vectors[i][j] for i in range(m)] for j in range(n)]
    print_matrix(vectors, n, m)

    gram = build_gram(*vectors)
    b = list(map(int, input(f"b = ").strip().split()))
    equation = extend_matrix(gram, n, n, [scalar_permutation(vec, b) for vec in vectors])

    solution = partial_solution(equation, n, n+1)
    print(solution)

    test(old_vectors, b, solution)


def graph():
    """
    Approximating random points with line
    """
    x_values = []
    y_values = []

    reg = LinearRegression()

    for i in range(5000):
        x_values.append(random.randint(0, 100))
        y_values.append(random.randint(0, 100))

        x = np.array(x_values)
        x = x.reshape(-1, 1)

        y = np.array(y_values)
        y = y.reshape(-1, 1)

        if i % 5 == 0:
            plt.clf()

            vectors = [[x_val, 1] for x_val in x_values]
            solution = solve(*vectors, right=y_values)
            k, b = solution

            reg.fit(x, y)
            plt.xlim(0, 100)
            plt.ylim(0, 100)
            plt.title(f"{k=:.5f}, {b=:.5f}")
            plt.scatter(x_values, y_values, color='black')
            plt.plot(list(range(100)), reg.predict(np.array([x for x in range(100)]).reshape(-1, 1)), color='blue')
            plt.plot(list(range(100)), [k*x + b for x in range(100)], color='red')
            plt.pause(0.0003)

    print("Finish")
    plt.show()


def parabola():
    """
    Approximation points with square polynom
    """
    points = [(0, 1), (1, 5), (2, 7), (3, 17), (4, 29)]
    vectors = [[x*x, x, 1] for x, y in points]
    solution = solve(*vectors, right=[y for x, y in points])
    a, b, c = solution
    print(solution)
    plt.plot(list(range(100)), [a*x*x + b*x + c for x in range(100)], color='red')
    plt.scatter([x for x, y in points], [y for x, y in points], color='black')
    plt.show()


if __name__ == '__main__':
    # main()
    graph()
    # parabola()
