import pytest
from app.transport_methods import northwest_corner, solve_transport_task, calculate_cost


def compare_matrix(a1, a2):
    if len(a1) != len(a2):
        return False
    for i in range(len(a1)):
        if len(a1[i]) != len(a2[i]):
            return False
        for j in range(len(a1[i])):
            if a1[i][j] != a2[i][j]:
                return False

    return True


cost_table = [[5, 3, 1], [3, 2, 4], [4, 1, 2]]
providers = [10, 20, 30]
consumers1 = [15, 20, 25]
consumers2 = [10, 20, 25]
northwest_corner_sol = [[10, ' ', ' '], [5, 15, ' '], [' ', 5, 25]]
solution = [[' ', ' ', 10], [15, 5, ' '], [' ', 15, 15]]
cost = 110


def test_northwest_corner():
    assert compare_matrix(northwest_corner(providers, consumers1), northwest_corner_sol) is True
    assert compare_matrix(northwest_corner(providers, consumers2), []) is True


def test_solve_transport_task():
    assert compare_matrix(solve_transport_task(northwest_corner_sol, cost_table), solution) is True


def test_calculate_cost():
    assert abs(calculate_cost(solution, cost_table) - cost) == 0
