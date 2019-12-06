import sys
from PyQt5.QtWidgets import QApplication
from .GUI import RoisTcToolbox


if __name__ == '__main__':
    modern = False
    app = QApplication(sys.argv)
    RoisTcToolbox = RoisTcToolbox(QApplication=app)
    RoisTcToolbox.show()
    sys.exit(app.exec_())
