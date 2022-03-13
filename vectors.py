from vec_exceptions import SizeMismatch
from itertools import combinations_with_replacement
from slae import transform


def add_vectors(left, right):
    if len(left) != len(right):
        raise SizeMismatch(f"Vector's size mismatch: {len(left)=}, {len(right)=}", left, right)
    return [left[i] + right[i] for i in range(len(left))]


def sub_vectors(left, right):
    if len(left) != len(right):
        raise SizeMismatch(f"Vector's size mismatch: {len(left)=}, {len(right)=}", left, right)
    return [left[i] - right[i] for i in range(len(left))]


def scale_vector(vec, alpha):
    return [elm*alpha for elm in vec]


def scalar_permutation(left: list, right: list):
    if len(left) != len(right):
        raise SizeMismatch(f"Vector's size mismatch: {len(left)=}, {len(right)=}", left, right)
    return sum(left[i]*right[i] for i in range(len(left)))


def build_gram(*vectors):
    n = len(vectors)
    matrix = [[0]*n for _ in range(n)]
    for i, j in combinations_with_replacement(range(n), 2):
        scalar = scalar_permutation(vectors[i], vectors[j])
        matrix[i][j] = scalar
        matrix[j][i] = scalar
    return matrix


def get_base(*vectors) -> list:
    """
    :param vectors: tuple of vectors with same length
    :return: base of vectors
    """
    assert len(vectors) != 0
    if min(len(vec) for vec in vectors) == max(len(vec) for vec in vectors):
        raise SizeMismatch("Vectors must be with same length")
    w = len(vectors[0])
    h = len(vectors)
    matrix = list(vectors)
    transform(matrix, h, w)
    return [matrix[i] for i in range(h) if any(matrix[i][j] for j in range(w))]


def matrix_vector_permutation(matrix: list[list], vector: list, n: int, m: int) -> list:
    """
    :param matrix: matrix m * n
    :param vector: vector of n elements
    :param n:
    :param m:
    :return: vector of m elements
    """
    return [sum(matrix[i][j]*vector[j] for j in range(n)) for i in range(m)]
