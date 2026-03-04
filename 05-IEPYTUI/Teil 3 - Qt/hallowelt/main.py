from qtpy import QtWidgets
import sys
import build  # hack para que compileUi funcione |||| quitar al acabar el dev.
from ui.mainwindow2 import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lename.setPlaceholderText("Tu nombre")
        self.ui.lenummer.setPlaceholderText("Tu teléfono")

        self.ui.pushButton.clicked.connect(self.print_message)
        self.ui.actionBeenden.triggered.connect(self.beenden)

    def beenden(self):
        sys.exit(0)

    def print_message(self):
        # 1) leer lo que insertó el cliente
        name = self.ui.lename.toPlainText().strip()
        telefon = self.ui.lenummer.toPlainText().strip()

        # validación mínima
        if not name or not telefon:
            self.ui.label.setText("Por favor escribe tu nombre y tu teléfono.")
            return

        # 3) imprimir en el label
        self.ui.label.setText(f"Hola {name},\nte llamaremos al telefono +49 {telefon} muy pronto 🙂")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()