from pathlib import Path
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from qtpy import QtWidgets

import build  # hack para que compileUi funcione |||| quitar al acabar el dev.
from database import Database
from ui.mainwindow2 import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # =========================
        # PSEUDOCÓDIGO (ARRANQUE)
        # =========================
        # 1) Cargar la UI (Qt Designer -> Ui_MainWindow)
        # 2) Preparar ruta a la base de datos y abrir conexión (Database)
        # 3) Conectar señales (botones, cambios de texto, Enter) con métodos
        # 4) Configurar tabla: columnas ocupan todo el ancho + estilo header
        # 5) Desactivar botón Guardar inicialmente y activar validación en vivo
        # =========================

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # [DB] Ruta relativa al archivo y creación del manager de DB
        self.database_path = Path(__file__).parent / "directorio.db"
        self.db = Database(self.database_path)

        # [UI] Conectar eventos
        self.elemente_verknuepfen()

        # [UI] Estado inicial del botón Guardar
        self.ui.speichernButton.setEnabled(False)

        # =========================
        # PSEUDOCÓDIGO (CONFIG TABLA)
        # =========================
        # 1) Hacer que las columnas se repartan el ancho disponible (sin huecos)
        # 2) Dar estilo al encabezado (verde, blanco, negrita)
        # =========================

        header = self.ui.twsuchen.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)    # ID angosto
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)             # Vorname
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)             # Nachname
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)    # Vorwahl angosta
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)             # Rufnummer
        self.ui.twsuchen.setColumnWidth(0, 50)

        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #039a4f;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        # [Menú] Acción salir
        self.ui.actionBeenden.triggered.connect(self.beenden)

    def elemente_verknuepfen(self):
        # =========================
        # PSEUDOCÓDIGO (EVENTOS UI)
        # =========================
        # 1) Botón "Buscar" -> buscar en DB y pintar resultados en tabla
        # 2) Botón "Guardar" -> leer formulario y guardar en DB
        # 3) En cada cambio de texto del formulario -> validar y habilitar/deshabilitar Guardar
        # 4) Tecla Enter: saltar entre campos y, al final, intentar guardar
        # 5) Setear estado inicial del botón según validación (por si hay texto prellenado)
        # =========================

        # [Clicks]
        self.ui.pbsuchen.clicked.connect(self.eintrag_suchen)
        self.ui.speichernButton.clicked.connect(self.hinzufuegen)

        # [Validación en vivo]
        for field in (self.ui.levorname, self.ui.lenachname, self.ui.levorwahl, self.ui.lerufnummer):
            field.textChanged.connect(self.eintraege_pruefen)

        # [Enter: navegación]
        self.ui.levorname.returnPressed.connect(self.ui.lenachname.setFocus)
        self.ui.lenachname.returnPressed.connect(self.ui.levorwahl.setFocus)
        self.ui.levorwahl.returnPressed.connect(self.ui.lerufnummer.setFocus)

        # [Enter en último campo: intentar guardar]
        self.ui.lerufnummer.returnPressed.connect(self.hinzufuegen)

        # [Estado inicial]
        self.eintraege_pruefen()

    def eintrag_suchen(self):
        # =========================
        # PSEUDOCÓDIGO (BUSCAR)
        # =========================
        # 1) Leer el término de búsqueda del input
        # 2) Consultar DB (eintrag_suchen)
        # 3) Limpiar tabla (contenido y filas)
        # 4) Insertar resultados fila por fila
        # 5) (Opcional) alinear/flags por columna (ej. ID centrado / no editable)
        # =========================

        suchbegriff = self.ui.lesuchen.text().strip()

        try:
            ergebnis = self.db.eintrag_suchen(suchbegriff)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Falló la búsqueda:\n{e}")
            return

        table = self.ui.twsuchen
        table.blockSignals(True)  # evita señales si luego agregas itemChanged, etc.
        table.clearContents()
        table.setRowCount(0)

        for fila in ergebnis:
            row = table.rowCount()
            table.insertRow(row)

            # fila = (id, vorname, nachname, vorwahl, rufnummer)
            for col, valor in enumerate(fila):
                item = QtWidgets.QTableWidgetItem(str(valor))

                # ID no editable
                if col == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                table.setItem(row, col, item)

        table.blockSignals(False)

    def hinzufuegen(self):
        # =========================
        # PSEUDOCÓDIGO (GUARDAR NUEVO CONTACTO)
        # =========================
        # 1) (Seguridad) Verificar que el botón está habilitado / datos válidos
        # 2) Leer campos del formulario
        # 3) Insertar en DB (eintrag_hinzufuegen)
        # 4) Limpiar formulario + deshabilitar botón Guardar
        # 5) (Opcional) refrescar tabla o mostrar mensaje de éxito
        # =========================

        # [1] Evitar guardar si no cumple validación (por ejemplo al presionar Enter)
        if not self.ui.speichernButton.isEnabled():
            return

        vorname = self.ui.levorname.text().strip()
        nachname = self.ui.lenachname.text().strip()
        vorwahl = self.ui.levorwahl.text().strip()
        telefon = self.ui.lerufnummer.text().strip()

        try:
            self.db.eintrag_hinzufuegen(vorname, nachname, vorwahl, telefon)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el registro:\n{e}")
            return

        # [4] Limpiar formulario (esto dispara textChanged y revalida)
        self.ui.levorname.clear()
        self.ui.lenachname.clear()
        self.ui.levorwahl.clear()
        self.ui.lerufnummer.clear()

        # [5 opcional] Feedback
        # QMessageBox.information(self, "OK", "Contacto guardado ✅")

    def eintraege_pruefen(self):
        # =========================
        # PSEUDOCÓDIGO (VALIDAR FORMULARIO)
        # =========================
        # 1) Nombre y apellido: deben tener texto (no solo espacios)
        # 2) Vorwahl y Rufnummer: deben ser numéricos (solo dígitos)
        # 3) Si todo está OK -> habilitar botón Guardar
        #    Si falta algo -> deshabilitar botón Guardar
        # =========================

        nombre_ok = bool(self.ui.levorname.text().strip())
        apellido_ok = bool(self.ui.lenachname.text().strip())
        telefono_ok = self.ui.lerufnummer.text().strip().isnumeric()
        vorwahl_ok = self.ui.levorwahl.text().strip().isnumeric()

        self.ui.speichernButton.setEnabled(nombre_ok and apellido_ok and telefono_ok and vorwahl_ok)

    def beenden(self):
        # =========================
        # PSEUDOCÓDIGO (SALIR)
        # =========================
        # 1) Cerrar conexión a DB
        # 2) Salir de la aplicación
        # =========================

        try:
            self.db.verbingung_schliessen()
        except Exception:
            pass

        QtWidgets.QApplication.quit()

    def closeEvent(self, event):
        # =========================
        # PSEUDOCÓDIGO (CONFIRMAR CIERRE)
        # =========================
        # 1) Preguntar al usuario si quiere cerrar
        # 2) Si confirma -> cerrar DB y aceptar
        # 3) Si no -> ignorar (cancelar cierre)
        # =========================

        reply = QMessageBox.question(
            self,
            "Program Schliessen?",
            "Soll das Programm wirklich beendet werden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.beenden()
            event.accept()
        else:
            event.ignore()


def main():
    # =========================
    # PSEUDOCÓDIGO (ENTRYPOINT)
    # =========================
    # 1) Crear QApplication
    # 2) Crear y mostrar MainWindow
    # 3) Iniciar loop de eventos
    # =========================

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
