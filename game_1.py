from PyQt6 import QtWidgets, QtCore
from random import randint

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        QtWidgets.QWidget.__init__(self, parent)
        self.attempts = 5
        self.live = QtWidgets.QLabel(f"Жизни: {self.attempts}")
        self.live.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.label = QtWidgets.QLabel("Введите число от 1 до 100")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.button_start = QtWidgets.QPushButton("Ответить")
        self.button_restart = QtWidgets.QPushButton("Еще раз")
        self.button_exit = QtWidgets.QPushButton("&Закрыть окно")
        self.number_user = randint(1, 100)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.live)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.lineEdit)
        self.vbox.addWidget(self.button_start)
        self.vbox.addWidget(self.button_restart)
        self.vbox.addWidget(self.button_exit)
        self.setLayout(self.vbox)
        self.button_start.clicked.connect(self.on_clicked)
        self.button_restart.clicked.connect(self.restart)
        self.button_exit.clicked.connect(QtWidgets.QApplication.instance().quit)

    def on_clicked(self):
        answer = int(self.lineEdit.text())
        self.lineEdit.clear()
        if answer == self.number_user:
            self.label.setText("Поздравляем! Вы угадали.")
        else:
            self.attempts -= 1
            self.live.setText(f"Жизни: {self.attempts}")
            if self.attempts == 0:
                self.label.setText(f"Вы проиграли! Загаданное число: {self.number_user}")
            else:
                if answer > self.number_user:
                    self.label.setText("Неправильно! Введите число меньше")
                if answer < self.number_user:
                    self.label.setText("Неправильно! Введите число больше")

    def restart(self):
        self.attempts = 5
        self.number_user = randint(1, 100)
        self.live.setText(f"Жизни: {self.attempts}")
        self.label.setText("Введите число от 1 до 100")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Угадай число!")
    window.resize(300, 250)
    window.show()
    sys.exit(app.exec())