import sys
from PyQt6.QtWidgets import QApplication

from src.ui import MeetingRecorderApp


def main():
    app = QApplication(sys.argv)
    ex = MeetingRecorderApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
