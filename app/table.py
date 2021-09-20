from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


def entering_number_create(text, cell):
    g_layout = QHBoxLayout()
    label = QLabel()
    label.setText(text)
    g_layout.addWidget(label)
    g_layout.addWidget(cell)

    return g_layout


def create_headers(columns, rows):
    A = ['A'+str(i+1) for i in range(rows)]
    B = ['B'+str(j+1) for j in range(columns)]
    A.append('b')
    B.append('a')

    return A, B


def number_cell(minimum):
    cell = QSpinBox()
    cell.setMinimum(minimum)

    return cell


def inactive_cell(value, active):
    cell = QTableWidgetItem()
    cell.setText(value)
    if active:
        cell.setFlags(Qt.ItemIsEnabled)

    return cell


def create_table(table, rows, columns):
    table.setColumnCount(columns + 1)
    table.setRowCount(rows + 1)

    A, B = create_headers(columns, rows)
    table.setHorizontalHeaderLabels(B)
    table.setVerticalHeaderLabels(A)

    return table


def input_table(table, rows, columns):
    table = create_table(table, rows, columns)

    for i in range(rows+1):
        for j in range(columns+1):
            if i == rows and j == columns:
                table.setItem(rows, columns, inactive_cell(' ', True))
            else:
                table.setCellWidget(i, j, number_cell(1))

    table.resizeColumnsToContents()

    return table


def show_table(table, c, a, b):
    rows = len(a)
    columns = len(b)
    table = create_table(table, rows, columns)

    for i in range(rows+1):
        for j in range(columns+1):
            if j == columns and i == rows:
                table.setItem(rows, columns, inactive_cell(' ', True))
            elif j == columns:
                table.setItem(i, columns, inactive_cell(str(a[i]), True))
            elif i == rows:
                table.setItem(rows, j, inactive_cell(str(b[j]), True))
            else:
                table.setItem(i, j, inactive_cell(str(c[i][j]), True))

    table.resizeColumnsToContents()

    return table
