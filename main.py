from gui import *

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec_()
