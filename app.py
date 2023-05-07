import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class MyThread(QThread):
    progress_updated = pyqtSignal(int)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        for i in range(101):
            self.progress_updated.emit(i)
            self.sleep(0.1)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Enter text:", self)
        self.label.move(50, 50)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(150, 50)

        self.button = QPushButton("Start", self)
        self.button.move(150, 100)
        self.button.clicked.connect(self.start_thread)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 150, 300, 25)

    def start_thread(self):
        text = self.line_edit.text()
        self.thread = MyThread(text)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
