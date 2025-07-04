from PyQt5 import QtWidgets, QtCore, QtGui
import styles

class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Medier - Interface')
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet(styles.get_central_widget_style())
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel('Medier')
        title.setFont(styles.get_retro_font())
        title.setStyleSheet(styles.get_title_label_style())
        layout.addWidget(title)

        open_btn = QtWidgets.QPushButton('Abrir Arquivo')
        open_btn.setStyleSheet(styles.get_button_style())
        layout.addWidget(open_btn)

        self.info_label = QtWidgets.QLabel('Nenhum arquivo carregado.')
        self.info_label.setStyleSheet(styles.get_media_info_style())
        layout.addWidget(self.info_label)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Interface()
    win.show()
    app.exec_()
