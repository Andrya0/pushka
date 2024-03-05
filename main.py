import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import Qt
from io import BytesIO

class Map(QMainWindow):
    def __init__(self):
        super().__init__()

        self.a = 55.751244
        self.b = 37.618423
        self.scale = 10
        self.min_scale = 1
        self.max_scale = 13

        self.setFixedSize(800, 800)

        self.load_map()

    def load_map(self):
        r_url = f"http://static-maps.yandex.ru/1.x/?ll={self.b},{self.a}&z={self.scale}&l=map&size=400,400"

        resp = requests.get(r_url)
        if resp.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(resp.content).read())

            pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio)

            m_label = self.findChild(QLabel)
            if m_label is None:
                m_label = QLabel(self)
            m_label.setPixmap(pixmap)
            m_label.setGeometry(0, 0, 800, 800)


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_PageUp:
            if self.scale < self.max_scale:
                self.scale += 1
                self.load_map()
        elif event.key() == Qt.Key_PageDown:
            if self.scale > self.min_scale:
                self.scale -= 1
                self.load_map()
        super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    map_app = Map()
    map_app.show()
    sys.exit(app.exec_())
