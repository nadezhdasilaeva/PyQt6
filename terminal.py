import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtCore import Qt
import sqlite3
from passage import EmployeeAccessApp

class SecurityTerminal(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Создаем поля ввода для данных охранника
        self.name_label = QLabel("Фамилия:")
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.username_label = QLabel("Имя:")
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.patronymic_label = QLabel("Отчество:")
        self.patronymic_input = QLineEdit(self)
        layout.addWidget(self.patronymic_label)
        layout.addWidget(self.patronymic_input)

        # Создаем кнопку для входа и выхода
        self.check_in_button = QPushButton('Войти', self)
        self.check_in_button.clicked.connect(self.check_in)
        layout.addWidget(self.check_in_button)

        self.check_out_button = QPushButton('Выйти', self)
        self.check_out_button.clicked.connect(self.check_out)
        layout.addWidget(self.check_out_button)

        self.passage_time_button = QPushButton('Временный пропуск', self)
        self.passage_time_button.clicked.connect(self.passage_time)
        layout.addWidget(self.passage_time_button)

        # Создаем метку для вывода сообщений
        self.message_label = QLabel(self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle('Учет посещаемости сотрудников')

    def check_in(self):
        # Получение данных от охранника
        first_name = self.name_input.text()
        second_name = self.username_input.text()
        last_name = self.patronymic_input.text()

        if first_name and second_name and last_name:
            connect = sqlite3.connect("base_data.db")
            cursor = connect.cursor()

            cursor.execute("select * from base_data where first_name = ? and second_name = ? and last_name = ?", (first_name, second_name, last_name))
            result = cursor.fetchone()

            if result:
                self.message_label.setText("Доступ разрешен")
                connect_2 = sqlite3.connect("base_data_2.db")
                cursor_2 = connect_2.cursor()
                time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)

                cursor_2.execute("INSERT INTO base_data_2 (first_name, second_name, entrance_time) VALUES (?, ?, ?)", (first_name, second_name, time))

                connect_2.commit()
                cursor_2.close()
                connect_2.close()
            else:
                self.message_label.setText("Доступ запрещен")
            connect.close()

    def check_out(self):
        # Получение данных от охранника
        first_name = self.name_input.text()
        second_name = self.username_input.text()
        last_name = self.patronymic_input.text()

        if first_name and second_name and last_name:
            connect = sqlite3.connect("base_data.db")
            cursor = connect.cursor()

            cursor.execute("select * from base_data where first_name = ? and second_name = ? and last_name = ?",
                           (first_name, second_name, last_name))
            result = cursor.fetchone()

            if result:
                self.message_label.setText("Доступ разрешен")
                connect_2 = sqlite3.connect("base_data_2.db")
                cursor_2 = connect_2.cursor()
                time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)

                cursor_2.execute("INSERT INTO base_data_2 (first_name, second_name, entrance_time) VALUES (?, ?, ?)", (first_name, second_name, time))

                connect_2.commit()
                cursor_2.close()
                connect_2.close()
            else:
                self.message_label.setText("Доступ запрещен")
            connect.close()

    def passage_time(self):
        self.terminal = EmployeeAccessApp()
        self.terminal.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SecurityTerminal()
    window.show()
    sys.exit(app.exec())