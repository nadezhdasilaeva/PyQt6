import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer, QDateTime, Qt
import sqlite3
import re

class EmployeeAccessApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Система временных пропусков")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()
        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)

        self.issue_access_button = QPushButton("Выдать пропуск")
        self.issue_access_button.clicked.connect(self.issue_access)
        self.layout.addWidget(self.issue_access_button)

        self.message_label = QLabel(self)
        self.layout.addWidget(self.message_label)

        self.conn = sqlite3.connect("base_data_2.db")
        self.cur = self.conn.cursor()

    def issue_access(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        current_time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        expiration_time = QDateTime.currentDateTime().addSecs(60).toString(Qt.DateFormat.ISODate)  # Пример: выдать пропуск на 1 минуту

        if not self.validate_name(name) or not self.validate_name(surname):
            self.message_label.setText("Некорректное имя или фамилия")
            return

        self.cur.execute("INSERT INTO base_data_2 (first_name, second_name, entrance_time, exit_time) VALUES (?, ?, ?, ?)", (surname, name, current_time, expiration_time))
        self.conn.commit()

        # Устанавливаем таймер на отзыв временного пропуска по истечении срока
        QTimer.singleShot(60 * 1000, lambda: self.revoke_access(name, surname))

        self.message_label.setText("Временный пропуск выдан")

    def revoke_access(self, name, surname):
        self.cur.execute("DELETE FROM base_data_2 WHERE first_name = ? AND second_name = ? AND expiration_time <= ?", (surname, name, QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)))
        self.conn.commit()

    def validate_name(self, name):
        if re.match(r'^[a-zA-Zа-яА-Я]+$', name):
            return True
        return False

def main():
    app = QApplication(sys.argv)
    window = EmployeeAccessApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
