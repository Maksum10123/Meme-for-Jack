import sys
import json
import random
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QDialog, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QIcon

class MemeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Мемасы от Джека')
        self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(QIcon('icon.ico'))
        
        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.label.setFixedSize(500, 500)

        self.categories_list = QListWidget(self)
        self.layout.addWidget(self.categories_list)

        self.load_button = QPushButton('Рандом Мэм', self)
        self.layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_meme)

        self.add_meme_button = QPushButton('Добавить мем в категорию', self)
        self.layout.addWidget(self.add_meme_button)
        self.add_meme_button.clicked.connect(self.add_meme)

        self.add_category_button = QPushButton('Добавить Категорию', self)
        self.layout.addWidget(self.add_category_button)
        self.add_category_button.clicked.connect(self.add_category)

        self.category_combo = QComboBox(self)
        self.layout.addWidget(self.category_combo)

        self.memes = {}
        self.load_memes()

    def load_memes(self):
        if os.path.exists('memes.json'):
            with open('memes.json', 'r') as file:
                self.memes = json.load(file)
                for category in self.memes.keys():
                    self.categories_list.addItem(QListWidgetItem(category))
                    self.category_combo.addItem(category)

    def load_meme(self):
        if self.categories_list.currentItem() is None:
            return
        category = self.categories_list.currentItem().text()
        if category in self.memes:
            meme = random.choice(self.memes[category])
            pixmap = QPixmap(meme)
            pixmap = pixmap.scaled(500, 500)
            self.label.setPixmap(pixmap)

    def add_meme(self):
        dialog = QDialog()
        dialog.setWindowTitle('Доавить мем')
        dialog.setGeometry(200, 200, 400, 150)
        layout = QVBoxLayout(dialog)

        self.category_combo = QComboBox(dialog)
        self.category_combo.addItems(self.memes.keys())
        layout.addWidget(self.category_combo)

        file_input = QLineEdit(dialog)
        layout.addWidget(file_input)

        file_button = QPushButton('Выбрать картинку', dialog)
        layout.addWidget(file_button)
        file_button.clicked.connect(lambda: self.select_file(file_input))

        save_button = QPushButton('Сохранить мем', dialog)
        layout.addWidget(save_button)
        save_button.clicked.connect(lambda: self.save_meme(self.category_combo.currentText(), file_input.text()))

        dialog.exec_()

    def select_file(self, file_input):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, 'Select Meme File', '', 'Images (*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.svg)', options=options)
        file_input.setText(file)

    def save_meme(self, category, file_path):
        if category not in self.memes:
            self.memes[category] = []
            self.categories_list.addItem(QListWidgetItem(category))
        self.memes[category].append(file_path)
        with open('memes.json', 'w') as file:
            json.dump(self.memes, file)

    def add_category(self):
        dialog = QDialog()
        dialog.setWindowTitle('Добавление категории')
        dialog.setGeometry(200, 200, 300, 100)
        layout = QVBoxLayout(dialog)

        category_input = QLineEdit(dialog)
        layout.addWidget(category_input)

        save_button = QPushButton('Добавить Категорию', dialog)
        layout.addWidget(save_button)
        save_button.clicked.connect(lambda: self.save_category(category_input.text()))

        dialog.exec_()

    def save_category(self, category):
        if category not in self.memes:
            self.memes[category] = []
            self.categories_list.addItem(QListWidgetItem(category))
            self.category_combo.addItem(category)
        with open('memes.json', 'w') as file:
            json.dump(self.memes, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    meme_generator = MemeGenerator()
    meme_generator.show()
    sys.exit(app.exec_())
