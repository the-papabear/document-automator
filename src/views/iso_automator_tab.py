from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class IsoUpdaterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("ISO FILE UPDATER COMMING SOON..."))
        self.setLayout(layout)