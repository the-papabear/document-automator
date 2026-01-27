import os
from datetime import datetime
from docx import Document
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel, 
    QPushButton, QFileDialog, QMessageBox
)

class DocumentGeneratorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MySeniorDevCo", "NameGenerator")
        self.template_file_path = None
        self.setup_ui()
        self.load_names()

    def setup_ui(self):
        layout = QVBoxLayout()

        # --- Adding Names Section ---
        add_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Type a name and press Enter...")
        self.name_input.returnPressed.connect(self.add_name_item)
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_name_item)
        
        add_layout.addWidget(self.name_input)
        add_layout.addWidget(add_btn)
        layout.addLayout(add_layout)

        # --- Select/Deselect All Buttons ---
        bulk_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        deselect_all_btn = QPushButton("Deselect All")
        
        # Using lambda for quick, simple connections
        select_all_btn.clicked.connect(lambda: self.toggle_all(Qt.Checked))
        deselect_all_btn.clicked.connect(lambda: self.toggle_all(Qt.Unchecked))
        
        bulk_layout.addWidget(select_all_btn)
        bulk_layout.addWidget(deselect_all_btn)
        layout.addLayout(bulk_layout)

        # --- The List ---
        layout.addWidget(QLabel("Double-click to edit, select to include:"))
        self.names_list = QListWidget()
        self.names_list.setSelectionMode(QListWidget.ExtendedSelection) # Allows multi-select for deletion
        self.names_list.model().dataChanged.connect(self.save_names)
        layout.addWidget(self.names_list)

        # ... (rest of your template selection and generate buttons) ...
        self.file_button = QPushButton("Select Template File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.template_label = QLabel("Template: None selected")
        layout.addWidget(self.template_label)

        self.generate_button = QPushButton("Generate Files")
        self.generate_button.clicked.connect(self.generate_files)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def toggle_all(self, state):
        """Sets the check state for every item in the list."""
        for i in range(self.names_list.count()):
            self.names_list.item(i).setCheckState(state)
        
    def add_name_item(self, name_text=None):
        """Creates a new checkable, editable list item."""
        # Handle both button click and direct string passing
        text = name_text if isinstance(name_text, str) else self.name_input.text().strip()
        
        if text:
            item = QListWidgetItem(text)
            # Flags: Checkable + Editable + Enabled + Selectable
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(Qt.Unchecked)
            self.names_list.addItem(item)
            self.name_input.clear()
            self.save_names()

    def save_names(self):
        """Serializes the list items into QSettings."""
        names = []
        for i in range(self.names_list.count()):
            names.append(self.names_list.item(i).text())
        self.settings.setValue("persisted_names", names)

    def load_names(self):
        """Hydrates the list from QSettings."""
        saved_names = self.settings.value("persisted_names", [])
        # Qt's value() might return a single string or list; ensure it's a list
        if isinstance(saved_names, str): saved_names = [saved_names]
        
        for name in saved_names:
            self.add_name_item(name)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.names_list.hasFocus():
            for item in self.names_list.selectedItems():
                self.names_list.takeItem(self.names_list.row(item))
            self.save_names()
        else:
            super().keyPressEvent(event)

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

        # FIX: Get only the names that are checked in the QListWidget
        selected_names = []
        for i in range(self.names_list.count()):
            item = self.names_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_names.append(item.text())

        if not selected_names:
            QMessageBox.warning(self, "Error", "Please check at least one name in the list.")
            return
        
        # Output setup
        timestamp = datetime.now().strftime("%d-%m_%Y-%H_%M_%S")
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        output_folder = os.path.join(downloads_folder, f"generated_files_{timestamp}")
        
        template_name_no_ext = os.path.splitext(os.path.basename(self.template_file_path))[0]
        os.makedirs(output_folder, exist_ok=True)

        for name in selected_names: # Using our filtered list
            doc = Document(self.template_file_path)
            for paragraph in doc.paragraphs:
                if "{{name}}" in paragraph.text:
                    paragraph.text = paragraph.text.replace("{{name}}", name)

            output_file = os.path.join(output_folder, f"{template_name_no_ext}-{name}.docx")
            doc.save(output_file)

        QMessageBox.information(self, "Success", f"{len(selected_names)} files created in {output_folder}")