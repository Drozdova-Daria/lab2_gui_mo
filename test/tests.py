import unittest
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


class TransportTaskTest(unittest.TestCase):
    def setUp(self):
        self.cost_table = [[5, 3, 1], [3, 2, 4], [4, 1, 2]]
        self.providers = [10, 20, 30]
        self.consumers1 = [15, 20, 25]
        self.consumers2 = [10, 20, 25]
        self.northwest_corner = [[10, ' ', ' '], [5, 15, ' '], [' ', 5, 25]]
        self.solution = [[' ', ' ', 10], [15, 5, ' '], [' ', 15, 15]]
        self.cost = 110

    def test_northwest_corner(self):
        message = 'northwest_corner returns an incorrect solution'
        self.assertTrue(compare_matrix(northwest_corner(self.providers, self.consumers1), self.northwest_corner),
                        msg=message)
        self.assertTrue(compare_matrix(northwest_corner(self.providers, self.consumers2), []), msg=message)

    def test_solve_transport_task(self):
        message = 'solve_transport_task return an incorrect solution'
        self.assertTrue(compare_matrix(solve_transport_task(self.northwest_corner, self.cost_table), self.solution),
                        msg=message)

    def test_calculate_cost(self):
        message = 'calculate_cost return an incorrect solution'
        self.assertEqual(abs(calculate_cost(self.solution, self.cost_table) - self.cost), 0, msg=message)