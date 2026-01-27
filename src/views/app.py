from PySide6.QtWidgets import QTabWidget, QMainWindow

from .document_generator_tab import DocumentGeneratorTab
from .iso_automator_tab import IsoUpdaterTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Automator")
        self.resize(640, 480)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(DocumentGeneratorTab(), "Document Generator")
        self.tabs.addTab(IsoUpdaterTab(), "ISO File Updater")