import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox
)
from docx import Document
from datetime import datetime

# ---------- Setup output folder ----------
timestamp = datetime.now().strftime("%d-%m_%Y-%H_%M_%S")
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
output_folder = os.path.join(downloads_folder, f"generated_files_{timestamp}")

# ---------- Application ----------
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Name Generator App")
window.setGeometry(100, 100, 400, 400)

layout = QVBoxLayout()

# Label
label = QLabel("Enter names (one per line):")
layout.addWidget(label)

# Text area for names
names_text = QTextEdit()
layout.addWidget(names_text)

# File selector
template_file_path = None

def select_file():
    global template_file_path
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Word Documents (*.docx)")
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            template_file_path = selected_files[0]
            template_label.setText(f"Template: {os.path.basename(template_file_path)}")

file_button = QPushButton("Select Template File")
file_button.clicked.connect(select_file)
layout.addWidget(file_button)

template_label = QLabel("Template: None selected")
layout.addWidget(template_label)

# Generate files button
def generate_files():
    global template_file_path
    if not template_file_path:
        QMessageBox.warning(window, "Error", "Please select a template file first.")
        return

    names = [n.strip() for n in names_text.toPlainText().splitlines() if n.strip()]
    if not names:
        QMessageBox.warning(window, "Error", "Please enter at least one name.")
        return
    
    template_name_no_ext = os.path.splitext(os.path.basename(template_file_path))[0]
    os.makedirs(output_folder, exist_ok=True)
    for name in names:
        doc = Document(template_file_path)
        # Replace placeholders in all paragraphs
        for paragraph in doc.paragraphs:
            if "{{name}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{name}}", name)

        output_file = os.path.join(output_folder, f"{template_name_no_ext}-{name}.docx")
        doc.save(output_file)

    QMessageBox.information(window, "Success", f"{len(names)} files created in {output_folder}")

generate_button = QPushButton("Generate Files")
generate_button.clicked.connect(generate_files)
layout.addWidget(generate_button)

# Set layout and show
window.setLayout(layout)
window.show()
sys.exit(app.exec())
