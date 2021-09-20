from table import *
from transport_methods import northwest_corner, solve_transport_task, calculate_cost, solve_transport_task_iterations, \
    print_system, print_potentials_solution, print_plan


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def check_close_issue(providers, consumers):
    if sum(providers) != sum(consumers):
        return False

    return True


def create_label(text, color='black'):
    label = QLabel()
    label.setText(text)
    label.setStyleSheet('color:' + color)

    return label


def create_button(text):
    button = QPushButton()
    button.setText(text)

    return button


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_value = 1
        self.m_value = 1

        self.c = [[1] * self.m_value for _ in range(self.n_value)]
        self.a = [1] * self.n_value
        self.b = [1] * self.m_value

        self.layout = QVBoxLayout()

        self.n = number_cell(1)
        self.m = number_cell(1)

        self.tr_table = None

        self.cr_table_g_layout = QGridLayout()
        self.solution_layout = QGridLayout()
        self.iterations_layout = QGridLayout()

        self.setup_ui()

        self.show()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_widget.setLayout(self.layout)

        self.setWindowTitle('Транспортная задача')

        self.layout.addLayout(entering_number_create('<b>Колличество поставщиков:</b>', self.n))
        self.layout.addLayout(entering_number_create('<b>Колличество потребителей:</b>', self.m))

        enter_n_m_button = create_button('Ввести')
        self.layout.addWidget(enter_n_m_button)
        enter_n_m_button.clicked.connect(self.get_table)

    def get_table(self):
        clearLayout(self.cr_table_g_layout)

        self.cr_table_g_layout.addWidget(create_label('<b>Введите транспортную таблицу:</b>'))

        self.n_value = self.n.value()
        self.m_value = self.m.value()
        self.tr_table = input_table(QTableWidget(self), self.n_value, self.m_value)
        self.cr_table_g_layout.addWidget(self.tr_table)

        enter_tr_table_button = create_button('Ввести')
        self.cr_table_g_layout.addWidget(enter_tr_table_button)
        enter_tr_table_button.clicked.connect(self.solution)

        self.layout.addLayout(self.cr_table_g_layout)

    def solution(self):
        clearLayout(self.solution_layout)

        self.c, self.a, self.b = self.read_table()

        if check_close_issue(self.a, self.b):
            self.solution_layout.addWidget(create_label('<b>Решение</b>'))

            self.solution_layout.addWidget(create_label('Опорный план, полученный методом северо-западного угла'))
            plan = northwest_corner(self.a, self.b)
            tr_table = show_table(QTableWidget(self), plan, self.a, self.b)
            self.solution_layout.addWidget(tr_table)

            self.solution_layout.addWidget(create_label('Решение, полученное методом потенциалов'))
            solution = solve_transport_task(plan, self.c)
            solution_table = show_table(QTableWidget(self), solution, self.a, self.b)
            self.solution_layout.addWidget(solution_table)

            summa = calculate_cost(solution, self.c)
            self.solution_layout.addWidget((create_label('Стоимость перевозки: ' + str(summa))))

            iterations_button = create_button('+ Показать шаги')
            self.solution_layout.addWidget(iterations_button)
            iterations_button.clicked.connect(self.iterations)
        else:
            self.solution_layout.addWidget(create_label('<b>Задача не является закрытой</b>', 'red'))

        self.layout.addLayout(self.solution_layout)

    def read_table(self):
        c = [[1] * self.m_value for _ in range(self.n_value)]
        a = [1] * self.n_value
        b = [1] * self.m_value

        for i in range(self.n_value):
            a[i] = self.tr_table.cellWidget(i, self.m_value).value()
            for j in range(self.m_value):
                c[i][j] = self.tr_table.cellWidget(i, j).value()

        for i in range(self.m_value):
            b[i] = self.tr_table.cellWidget(self.n_value, i).value()

        return c, a, b

    def iterations(self):
        clearLayout(self.iterations_layout)

        line = QTextEdit()
        line.setReadOnly(True)

        iterations = solve_transport_task_iterations(northwest_corner(self.a, self.b), self.c)
        number_iteration = 1

        for iteration in iterations:
            line.append('<b>Шаг ' + str(number_iteration) + '</b>\n')
            line.append(print_system(iteration[2], self.c))
            line.append(print_potentials_solution(iteration[0], iteration[1]))
            line.append('Текущий план:')
            line.append(print_plan(iteration[2]))

            number_iteration += 1

        self.iterations_layout.addWidget(line)
        self.layout.addLayout(self.iterations_layout)
