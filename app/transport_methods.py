import numpy

directions = [[-1, 0], [0, 1], [0, -1], [1, 0]]


def northwest_corner(providers, consumers):
    if sum(providers) != sum(consumers):
        return []

    n = len(providers)
    m = len(consumers)

    reference_solution = [[' '] * m for _ in range(n)]
    _providers = list(providers)
    _consumers = list(consumers)

    position_x = 0
    position_y = 0

    while position_x != n and position_y != m:
        reference_solution[position_x][position_y] = min(_providers[position_x], _consumers[position_y])
        _providers[position_x] = _providers[position_x] - reference_solution[position_x][position_y]
        _consumers[position_y] = _consumers[position_y] - reference_solution[position_x][position_y]
        if _providers[position_x] != 0:
            position_y = position_y + 1
        else:
            position_x = position_x + 1

    return reference_solution


def build_system(ref_plan, cost_table):
    n = len(ref_plan)
    m = len(ref_plan[0])

    A = [[0] * (n + m - 1) for _ in range(n + m - 1)]
    _b = list()

    count = 0

    for i in range(n):
        for j in range(m):
            if ref_plan[i][j] != ' ':
                _b.append(cost_table[i][j])
                if i != 0:
                    A[count][m + i - 1] = 1
                A[count][j] = 1
                count += 1

    return A, _b


def check_optimal_plan(u_providers, v_consumers, ref_plan, cost_table):
    for i in range(len(u_providers)):
        for j in range(len(v_consumers)):
            if ref_plan[i][j] == ' ':
                if v_consumers[j] + u_providers[i] > cost_table[i][j]:
                    return False

    return True


def solve_system(ref_plan, cost_table):
    A, _b = build_system(ref_plan, cost_table)

    solve = numpy.linalg.solve(A, _b)

    _v = list(solve[:len(ref_plan[0])])
    _u = list([0]) + list(solve[len(ref_plan[0]):])

    return _u, _v


def step(point, direction):
    return [point[0] + direction[0], point[1] + direction[1]]


def point_num(point, hor_size):
    return point[0] * hor_size + point[1]


def equal_point(point, point_2):
    return point[0] == point_2[0] and point[1] == point_2[1]


def walk(point, current_direction, ref_plan, starting_point, visited, prev_point):
    point_id = point_num(point, len(ref_plan[0]))

    if point[0] < 0 or point[1] < 0 or point[0] >= len(ref_plan) \
            or point[1] >= len(ref_plan[0]) or (point_id in visited):
        return False, []

    nul = (ref_plan[point[0]][point[1]] != ' ')
    visited.add(point_id)

    if not nul:
        if point[0] == starting_point[0] and point[1] == starting_point[1]:
            return True, []

        next_point = step(point, current_direction)
        find, path = walk(next_point, current_direction, ref_plan, starting_point, visited, point)

        if find:
            return find, path

        visited.remove(point_id)
    else:
        for direction in directions:
            next_point = step(point, direction)

            if equal_point(next_point, prev_point):
                continue

            find, path = walk(next_point, direction, ref_plan, starting_point, visited, point)

            if not equal_point(direction, current_direction):
                path.append(point)

            if find:
                return find, path

        visited.remove(point_id)

    return False, []


def find_new_working_point(v_providers, u_consumers, ref_plan, cost_table):
    maximum = 0
    point = [0, 0]

    for i in range(len(ref_plan)):
        for j in range(len(ref_plan[0])):
            if ref_plan[i][j] == ' ':
                if (u_consumers[j] + v_providers[i] - cost_table[i][j]) > maximum:
                    maximum = abs(u_consumers[j] + v_providers[i] - cost_table[i][j])
                    point = [i, j]

    return point


def find_min(way, ref_plan):
    min_elem = ref_plan[way[0][0]][way[0][1]]
    point = [way[0][0], way[0][1]]

    for elem in way:
        if elem[2] == '-':
            if ref_plan[elem[0]][elem[1]] < min_elem:
                point = [elem[0], elem[1]]
                min_elem = ref_plan[elem[0]][elem[1]]

    return min_elem, point


def find_way(starting_point, ref_plan):
    for direction in directions:
        next_point = step(starting_point, direction)
        find, path = walk(next_point, direction, ref_plan, starting_point, set(), starting_point)
        if find:
            return path

    return


def change_plan(ref_plan, start_point):
    way = find_way(start_point, ref_plan)
    minus = True

    for i in range(len(way)):
        if minus:
            way[i].append("-")
        else:
            way[i].append("+")
        minus = not minus

    minimum, min_point = find_min(way, ref_plan)
    ref_plan[start_point[0]][start_point[1]] = minimum

    for elem in way:
        if elem[2] == '-' and elem[0] == min_point[0] and elem[1] == min_point[1]:
            ref_plan[elem[0]][elem[1]] = ' '
        elif elem[2] == "-":
            ref_plan[elem[0]][elem[1]] -= minimum
        else:
            ref_plan[elem[0]][elem[1]] += minimum

    return ref_plan


def solve_transport_task(plan, cost_table):
    while True:
        u, v = solve_system(plan, cost_table)
        if not check_optimal_plan(u, v, plan, cost_table):
            working_point = find_new_working_point(u, v, plan, cost_table)
            plan = change_plan(plan, working_point)
        else:
            break

    return plan


def solve_transport_task_iterations(plan, cost_table):
    while True:
        u, v = solve_system(plan, cost_table)
        yield u, v, plan
        if not check_optimal_plan(u, v, plan, cost_table):
            working_point = find_new_working_point(u, v, plan, cost_table)
            plan = change_plan(plan, working_point)
        else:
            break


def print_system(plan, c):
    equations = ''
    for i in range(len(plan)):
        for j in range(len(plan[i])):
            if plan[i][j] != ' ':
                equations += ('v' + str(j + 1) + ' + u' + str(i + 1) + ' = ' + str(c[i][j]) + '\n')

    return equations


def print_potentials_solution(u, v):
    string = ''
    for i in range(len(u)):
        string += 'u' + str(i + 1) + ' = ' + str(u[i]) + '; '
    for i in range(len(v)):
        string += 'u' + str(i + 1) + ' = ' + str(v[i]) + '; '

    return string + '\n'


def calculate_cost(plan, cost_table):
    summa = 0
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] != ' ':
                summa += plan[i][j] * cost_table[i][j]

    return summa


def print_plan(plan):
    string_plan = '<table border="1" cellspacing="0" >'
    for i in range(len(plan)):
        string_plan += '<tr>'
        for j in range(len(plan[i])):
            string_plan += '<td>' + str(plan[i][j]) + '</td>'
        string_plan += '</tr>'

    return string_plan + '</table>'
