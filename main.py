import sys
sys.dont_write_bytecode = True
from Ui.app import MainWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    stylesheet = MainWindow.load_stylesheet("style.css")
    if stylesheet:
        app.setStyleSheet(stylesheet)
        print("✅")
    else:
        print("⚠️")
    
    window = MainWindow()
    sys.exit(app.exec())