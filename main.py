import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
import sqlite3

Ui_InvWindow, baseClass = uic.loadUiType('Design.ui')

# PROBLEM FOR SUNDAY (7/9/23): FIX ADDITEM BUTTON SO IT SHOWS ON EACH CATEGORY (FIXED)


class MainWindow(baseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_InvWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.EditButton.clicked.connect(self.enable_add_button)
        self.ui.ReportButton.clicked.connect(self.disable_add_button)
        self.ui.AddItem.clicked.connect(self.add_item_popup)

        self.db_conn = sqlite3.connect('inventory.db')
        self.db_cursor = self.db_conn.cursor()
        self.create_table()

    def enable_add_button(self):
        self.ui.AddItem.setEnabled(True)

    def disable_add_button(self):
        self.ui.AddItem.setEnabled(False)

    def add_item_popup(self):
        category = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        item, ok = qtw.QInputDialog.getText(self, 'Add Item', f'Enter item for {category}')
        if ok and item:
            quantity, ok = qtw.QInputDialog.getInt(self, 'Add Item', f'Enter quantity for {item}')
            if ok:
                barcode_id, ok = qtw.QInputDialog.getText(self, 'Add Item', f'Enter barcode ID for {item}')
                if ok and barcode_id:
                    uuid, ok = qtw.QInputDialog.getText(self, 'Add Item', f'Enter UUID for {item}')
                    if ok and uuid:
                        self.save_item(category, item, quantity, barcode_id, uuid)
                        self.update_table(category)

    def save_item(self, category, item, quantity, barcode_id, uuid):
        query = "INSERT INTO items (category, item_name, quantity, barcode_id, uuid) VALUES (?, ?, ?, ?, ?)"
        values = (category, item, quantity, barcode_id, uuid)
        self.db_cursor.execute(query, values)
        self.db_conn.commit()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            item_name TEXT,
            quantity INTEGER,
            barcode_id TEXT,
            uuid TEXT
        );'''
        self.db_cursor.execute(query)
        self.db_conn.commit()

    def update_table(self, category):
        query = "SELECT * FROM items WHERE category = ?"
        self.db_cursor.execute(query, (category,))
        items = self.db_cursor.fetchall()
        row_count = len(items)

        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.indexOf(self.ui.tab))
        self.ui.tableWidget.setRowCount(row_count)

        for row, item in enumerate(items):
            for col, value in enumerate(item[1:]):
                self.ui.tableWidget.setItem(row, col, qtw.QTableWidgetItem(str(value)))

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
