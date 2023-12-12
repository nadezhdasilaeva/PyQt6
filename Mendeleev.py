from PyQt6 import QtWidgets
from ui_mainwindow import Ui_MainWindow
import csv


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        super().__init__()
        self.setupUi(self)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(53)
        self.pushButton.clicked.connect(self.on_clicked)

    def on_clicked(self):
        self.textEdit.clear()
        file = open('periodictable.csv').readlines()
        reader = csv.reader(file)
        el = list(reader)
        file.clear()

        columns = ['Atomic Number', 'Symbol', 'Element', 'Origin of name', 'Group', 'Period', 'Atomic weight',
                   'Density',
                   'Melting point', 'Boiling point', 'Specific heat capacity', 'Electronegativity',
                   'Abundance in earth`s crust']

        cout_col = 0
        for i in columns:
            if len(i) > cout_col:
                cout_col = len(i)
        el_data = {}
        for i in el:
            element = {'Atomic Number': i[0],
                       'Symbol': i[1],
                       'Element': i[2],
                       'Origin of name': i[3],
                       'Group': i[4],
                       'Period': i[5],
                       'Atomic weight': i[6],
                       'Density': i[7],
                       'Melting point': i[8],
                       'Boiling point': i[9],
                       'Specific heat capacity': i[10],
                       'Electronegativity': i[11],
                       'Abundance in earth`s crust': i[12]}
            el_data[i[0]] = element
            el_data[i[1]] = element

        answer = self.lineEdit.text()
        self.lineEdit.clear()
        if answer in el_data:
            for i in columns:
                true = i.rjust(cout_col)
                self.textEdit.append(true + ': ' + el_data[answer][i])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())