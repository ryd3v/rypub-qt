import sys
import ebooklib
from ebooklib import epub
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QToolBar, QTextBrowser, QStyleFactory
from PyQt6.QtGui import QIcon

class EPubReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle('EPub Reader')
        self.setGeometry(100, 100, 800, 600)

        # ebup reader class
        self.textBrowser = QTextBrowser()
        self.textBrowser.setReadOnly(True)
        self.textBrowser.verticalScrollBar().setVisible(False)
        self.setCentralWidget(self.textBrowser)
        self.current_file_path = ''

        self.createToolBar()
        self.createMenu()

    def createToolBar(self):
        tool_bar = QToolBar('Toolbar')
        self.addToolBar(tool_bar)

        # Create a toggle theme action with a default label
        self.toggle_theme_action = QAction(QIcon('icons/sun.png'), '', self)
        self.toggle_theme_action.triggered.connect(self.toggleTheme)
        tool_bar.addAction(self.toggle_theme_action)

        # Assume light mode is the default; adjust as necessary
        self.current_theme = 'dark'

    def toggleTheme(self):
        if self.current_theme == 'light':
            self.changeTheme('dark')
            self.toggle_theme_action.setIcon(QIcon('icons/moon.png'))  # Moon emoji for dark mode
            self.current_theme = 'dark'
        else:
            self.changeTheme('light')
            self.toggle_theme_action.setIcon(QIcon('icons/sun.png'))  # Sun emoji for light mode
            self.current_theme = 'light'



    def createMenu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu('File')
        open_file_action = QAction('Open File', self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open EPub File', '.', 'EPub Files (*.epub)')
        if file_path:
            self.current_file_path = file_path
            self.display_file()

    def changeTheme(self, theme):
        palette = QPalette()
        if theme == 'light':
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

            self.textBrowser.setStyleSheet("background-color: white; color: black;")
        elif theme == 'dark':
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

            self.textBrowser.setStyleSheet("background-color: black; color: white;")
    
        QApplication.setPalette(palette)



    def display_file(self):
        if not self.current_file_path:
            return
        try:
            book = epub.read_epub(self.current_file_path)
            html_content = ''
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    html_content += item.get_body_content().decode('utf-8')
            self.textBrowser.setHtml(html_content)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            # Turn page to the left
            pass
        elif event.key() == Qt.Key.Key_Right:
            # Turn page to the right
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = EPubReader()
    reader.show()
    sys.exit(app.exec())
