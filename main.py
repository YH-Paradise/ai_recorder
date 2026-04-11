# main.py (최상단 폴더에 위치)
import sys
from PyQt6.QtWidgets import QApplication

# 핵심 로직이 들어있는 src 폴더에서 UI를 불러옵니다.
from src.ui import MeetingRecorderApp

def main():
    app = QApplication(sys.argv)
    ex = MeetingRecorderApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()