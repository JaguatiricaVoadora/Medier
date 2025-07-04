from PyQt5 import QtGui

def get_retro_font():
    return QtGui.QFont('Courier New', 10, QtGui.QFont.Bold)

def get_button_style():
    return """
        QPushButton {
            background-color: #111;
            color: #FFD700;
            border: 2px solid #FFD700;
            border-radius: 6px;
            padding: 3px 7px;
        }
        QPushButton:hover {
            background-color: #FFD700;
            color: #111;
        }
    """

def get_titlebar_style():
    return "background-color: #111; border-bottom: 2px solid #FFD700;"

def get_title_label_style():
    return "color: #FFD700; letter-spacing: 3px;"

def get_videoframe_style():
    return "border: 2px solid #FFD700; border-radius: 5px;"

def get_visualizer_style():
    return "background-color: #111; border-top: 1px solid #555;"

def get_position_slider_style():
    return """
        QSlider::groove:horizontal {
            background: #FFD700;
            height: 6px;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #111;
            border: 2px solid #FFD700;
            width: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }
    """

def get_central_widget_style():
    return "background-color: #121212; color: #FFD700;"

def get_media_info_style():
    return "color: #FFD700; padding-left: 10px;"
