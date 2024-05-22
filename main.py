import sys
import os
import ebooklib
import base64
from ebooklib import epub
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTextBrowser,
    QStyleFactory,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QFontDatabase, QFont


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_fonts_from_directory(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".ttf") or file_name.endswith(".otf"):
            font_path = os.path.join(directory, file_name)
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print(f"Failed to load font at {font_path}")
            else:
                print(f"Loaded font at {font_path}")


icon = resource_path("icon.ico")
bulb_icon = resource_path("bulb.png")


class EPubReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(icon))
        self.initUI()

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.setWindowTitle("ryPub EPub Reader")
        self.setGeometry(100, 100, 600, 800)

        self.textBrowser = QTextBrowser()
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.verticalScrollBar().setVisible(False)
        self.textBrowser.horizontalScrollBar().setVisible(False)
        self.setCentralWidget(self.textBrowser)
        self.current_file_path = ""
        self.createMenu()

    def toggleTheme(self):
        if self.current_theme == "light":
            self.changeTheme("dark")
            self.toggle_theme_action = QAction(
                QIcon(resource_path(bulb_icon)), "Light Mode", self
            )
            self.toggle_theme_action.setText("Light Mode")
            self.current_theme = "dark"
        else:
            self.changeTheme("light")
            self.toggle_theme_action.setIcon(QIcon(resource_path(bulb_icon)))
            self.toggle_theme_action.setText("Dark Mode")
            self.current_theme = "light"

    def createMenu(self):
        menu = self.menuBar()
        self.current_theme = "dark"
        file_menu = menu.addMenu("File")
        open_file_action = QAction("Open File", self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        self.toggle_theme_action = QAction(QIcon(bulb_icon), "Light Mode", self)
        self.toggle_theme_action.triggered.connect(self.toggleTheme)
        file_menu.addAction(self.toggle_theme_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open EPub File", ".", "EPub Files (*.epub)"
        )
        if file_path:
            self.current_file_path = file_path
            self.display_file()

    def changeTheme(self, theme):
        palette = QPalette()
        if theme == "light":
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

            self.textBrowser.setStyleSheet("background-color: white; color: black;")
        elif theme == "dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

            self.textBrowser.setStyleSheet("background-color: #2d2d2d; color: white;")

        QApplication.setPalette(palette)

    def display_file(self):
        if not self.current_file_path:
            return
        try:
            book = epub.read_epub(self.current_file_path)
            html_content = "<style>img { max-width: 100%; height: auto; }</style>"
            images_data_urls = {}

            for item in book.get_items():
                if isinstance(item, epub.EpubImage):
                    image_data = item.get_content()
                    data_url = "data:image/{};base64,{}".format(
                        item.media_type.split("/")[-1],
                        base64.b64encode(image_data).decode("utf-8"),
                    )
                    images_data_urls[item.file_name] = data_url

            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    html = item.get_content().decode("utf-8")
                    for original_path, data_url in images_data_urls.items():
                        html = html.replace(original_path, data_url)
                    html_content += html

            self.textBrowser.setHtml(html_content)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            pass
        elif event.key() == Qt.Key.Key_Right:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fonts_directory = resource_path(".")
    load_fonts_from_directory(fonts_directory)
    roboto_font = QFont("Roboto-Regular")
    monospaced_font = QFont("JetBrainsMono-Regular")
    monospaced_font.setPointSize(12)
    app.setFont(roboto_font)
    reader = EPubReader()
    reader.show()
    sys.exit(app.exec())
