import sys
import os
from datetime import datetime
from docx import Document
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, 
    QPushButton, QFileDialog, QMessageBox, QTabWidget, QMainWindow
)

class GeneratorTab(QWidget):
    """The existing Name Generator logic encapsulated in a tab."""
    def __init__(self):
        super().__init__()
        self.template_file_path = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input Section
        layout.addWidget(QLabel("Enter names (one per line):"))
        self.names_text = QTextEdit()
        layout.addWidget(self.names_text)

        # Template Selection
        self.file_button = QPushButton("Select Template File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.template_label = QLabel("Template: None selected")
        layout.addWidget(self.template_label)

        # Generate Action
        self.generate_button = QPushButton("Generate Files")
        self.generate_button.clicked.connect(self.generate_files)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Word Documents (*.docx)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.template_file_path = selected_files[0]
                self.template_label.setText(f"Template: {os.path.basename(self.template_file_path)}")

    def generate_files(self):
        if not self.template_file_path:
            QMessageBox.warning(self, "Error", "Please select a template file first.")
            return

        names = [n.strip() for n in self.names_text.toPlainText().splitlines() if n.strip()]
        if not names:
            QMessageBox.warning(self, "Error", "Please enter at least one name.")
            return
        
        # Output setup
        timestamp = datetime.now().strftime("%d-%m_%Y-%H_%M_%S")
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        output_folder = os.path.join(downloads_folder, f"generated_files_{timestamp}")
        
        template_name_no_ext = os.path.splitext(os.path.basename(self.template_file_path))[0]
        os.makedirs(output_folder, exist_ok=True)

        for name in names:
            doc = Document(self.template_file_path)
            for paragraph in doc.paragraphs:
                if "{{name}}" in paragraph.text:
                    paragraph.text = paragraph.text.replace("{{name}}", name)

            output_file = os.path.join(output_folder, f"{template_name_no_ext}-{name}.docx")
            doc.save(output_file)

        QMessageBox.information(self, "Success", f"{len(names)} files created in {output_folder}")

class FutureTab(QWidget):
    """Placeholder for your future feature."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🚀 Future Feature Coming Soon!"))
        layout.addStretch() # Pushes content to the top
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Name Generator App v2.0")
        self.resize(450, 500)

        # Central Widget & Main Layout
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add Tabs
        self.tabs.addTab(GeneratorTab(), "Name Generator")
        self.tabs.addTab(FutureTab(), "Advanced Settings")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())