import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
import vlc

import styles  # Importa o módulo de estilos

class VisualizerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bars = 20
        self.bar_heights = [0]*self.bars
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_bars)
        self.setFixedHeight(20)
        self.setStyleSheet(styles.get_visualizer_style())

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()
        self.bar_heights = [0]*self.bars
        self.update()

    def update_bars(self):
        for i in range(self.bars):
            change = random.randint(-2, 4)
            new_height = self.bar_heights[i] + change
            self.bar_heights[i] = max(1, min(15, new_height))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        w = self.width()
        h = self.height()
        bar_width = w / self.bars
        painter.setBrush(QtGui.QColor(255, 215, 0))
        painter.setPen(QtCore.Qt.NoPen)
        for i, height in enumerate(self.bar_heights):
            x = int(i * bar_width)
            bw = int(bar_width * 0.7)
            bh = int(height)
            painter.drawRect(x, h - bh, bw, bh)

class PlayerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medier')
        self.setGeometry(100, 100, 900, 540)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.is_paused = False
        self.old_pos = None
        self.is_fullscreen = False
        self.init_ui()

    def init_ui(self):
        retro_font = styles.get_retro_font()

        # Frame vídeo
        self.videoframe = QtWidgets.QFrame()
        pal = self.videoframe.palette()
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(20, 20, 20))
        self.videoframe.setPalette(pal)
        self.videoframe.setAutoFillBackground(True)
        self.videoframe.setStyleSheet(styles.get_videoframe_style())

        # Barra título
        self.titlebar = QtWidgets.QWidget()
        self.titlebar.setFixedHeight(30)
        self.titlebar.setStyleSheet(styles.get_titlebar_style())
        title_layout = QtWidgets.QHBoxLayout(self.titlebar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        self.title_label = QtWidgets.QLabel("Medier")
        self.title_label.setFont(QtGui.QFont('Courier New', 13, QtGui.QFont.Bold))
        self.title_label.setStyleSheet(styles.get_title_label_style())
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_layout.addWidget(self.title_label, 1)

        self.min_btn = QtWidgets.QPushButton('–')
        self.close_btn = QtWidgets.QPushButton('✕')
        for btn in (self.min_btn, self.close_btn):
            btn.setFixedSize(26, 26)
            btn.setFont(retro_font)
            btn.setStyleSheet(styles.get_button_style())
        self.min_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)
        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.close_btn)

        # Botões controles
        self.play_btn = QtWidgets.QPushButton('▶')
        self.pause_btn = QtWidgets.QPushButton('❚❚')
        self.stop_btn = QtWidgets.QPushButton('■')
        self.open_btn = QtWidgets.QPushButton('☰')
        self.fullscreen_btn = QtWidgets.QPushButton('⛶')
        for btn in (self.open_btn, self.play_btn, self.pause_btn, self.stop_btn, self.fullscreen_btn):
            btn.setFixedSize(40, 30)
            btn.setFont(retro_font)
            btn.setStyleSheet(styles.get_button_style())

        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.position_slider.setMaximum(1000)
        self.position_slider.setFixedHeight(14)
        self.position_slider.setStyleSheet(styles.get_position_slider_style())

        self.media_info = QtWidgets.QLabel("00:00 / 00:00")
        self.media_info.setFont(QtGui.QFont('Courier New', 9))
        self.media_info.setStyleSheet(styles.get_media_info_style())

        self.visualizer = VisualizerWidget()

        self.playlist = QtWidgets.QListWidget()

        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.setSpacing(10)
        for btn in (self.open_btn, self.play_btn, self.pause_btn, self.stop_btn, self.fullscreen_btn):
            controls_layout.addWidget(btn)
        controls_layout.addWidget(self.position_slider, 1)
        controls_layout.addWidget(self.media_info)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        main_layout.addWidget(self.titlebar)
        main_layout.addWidget(self.videoframe, 1)
        main_layout.addWidget(self.visualizer)
        main_layout.addLayout(controls_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet(styles.get_central_widget_style())
        self.setCentralWidget(central_widget)
        self.setFont(retro_font)

        self.titlebar.mousePressEvent = self.titlebar_mousePressEvent
        self.titlebar.mouseMoveEvent = self.titlebar_mouseMoveEvent

        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.play_media)
        self.pause_btn.clicked.connect(self.pause_media)
        self.stop_btn.clicked.connect(self.stop_media)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        self.videoframe.mouseDoubleClickEvent = self.toggle_fullscreen_event

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_ui)

        QtWidgets.QShortcut(QtGui.QKeySequence('F11'), self, self.toggle_fullscreen)

    def open_file(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            'Abrir arquivos',
            '.',
            'Todos os arquivos de mídia (*.mp4 *.mp3 *.avi *.mkv *.mov *.mpg *.mpeg *.wmv *.flv *.webm *.flac *.wav *.ogg *.aac *.wma *.m4a);;Vídeo (*.mp4 *.avi *.mkv *.mov *.mpg *.mpeg *.wmv *.flv *.webm);;Áudio (*.mp3 *.flac *.wav *.ogg *.aac *.wma *.m4a)'
        )
        if files:
            for f in files:
                if f not in [self.playlist.item(i).text() for i in range(self.playlist.count())]:
                    self.playlist.addItem(f)
            self.playlist.setCurrentRow(self.playlist.count()-1)
            self.play_selected()

    def play_selected(self):
        current_item = self.playlist.currentItem()
        if current_item:
            filename = current_item.text()
            media = self.instance.media_new(filename)
            self.mediaplayer.set_media(media)
            if sys.platform.startswith('linux'):
                self.mediaplayer.set_xwindow(self.videoframe.winId())
            elif sys.platform == 'win32':
                self.mediaplayer.set_hwnd(self.videoframe.winId())
            elif sys.platform == 'darwin':
                self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
            self.mediaplayer.play()
            self.timer.start()
            self.is_paused = False
            self.visualizer.start()

    def play_media(self):
        if self.mediaplayer.play() == -1:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Não consegui tocar o arquivo.')
        else:
            self.timer.start()
            self.is_paused = False
            self.visualizer.start()

    def pause_media(self):
        self.mediaplayer.pause()
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.visualizer.stop()
        else:
            self.visualizer.start()

    def stop_media(self):
        self.mediaplayer.stop()
        self.timer.stop()
        self.visualizer.stop()

    def set_position(self, position):
        self.mediaplayer.set_position(position / 1000.0)

    def update_ui(self):
        if not self.mediaplayer.is_playing():
            self.timer.stop()
            if not self.is_paused:
                self.stop_media()
        else:
            pos = int(self.mediaplayer.get_position() * 1000)
            self.position_slider.setValue(pos)

        length = self.mediaplayer.get_length() // 1000
        cur = self.mediaplayer.get_time() // 1000
        mins, secs = divmod(cur, 60)
        tmins, tsecs = divmod(length, 60)
        res = (self.mediaplayer.video_get_width(), self.mediaplayer.video_get_height())
        codec = ''
        if self.mediaplayer.get_media():
            mrl = self.mediaplayer.get_media().get_mrl()
            codec = mrl.split('.')[-1].upper()
        self.media_info.setText(f'{mins:02}:{secs:02} / {tmins:02}:{tsecs:02}   {res[0]}x{res[1]} {codec}')

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.showFullScreen()
            self.titlebar.hide()
            self.visualizer.hide()
            self.is_fullscreen = True
        else:
            self.showNormal()
            self.titlebar.show()
            self.visualizer.show()
            self.is_fullscreen = False

    def toggle_fullscreen_event(self, event):
        self.toggle_fullscreen()

    def titlebar_mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()

    def titlebar_mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = PlayerWindow()
    player.show()
    sys.exit(app.exec_())
