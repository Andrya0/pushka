import os.path
import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from pip._vendor import requests


class MapParams(object):
    def __init__(self):
        self.lat = 61.665279
        self.lon = 50.839492
        self.zoom = 16
        self.type = "map"  # "sat", "sat,skl"

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    def update(self, event):
        if event.key() == Qt.Page_UP and self.zoom < 19:
            self.zoom += 1
        elif event.key() == Qt.Key_Page_DOWN and self.zoom > 2:
            self.zoom -= 1


class WindowMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)  # Загружаем дизайн
        self.initUI()
        self.pushButton.clicked.connect(self.search)

    def initUI(self):
        self.setWindowTitle('Отображение картинки')
        load_map(MapParams())
        if os.path.exists('map.png'):
            ## Изображение
            self.pixmap = QPixmap('map.png')
            # Если картинки нет, то QPixmap будет пустым,
            # а исключения не будет
            self.image = QLabel(self)
            self.image.move(80, 60)
            self.image.resize(250, 250)
            # Отображаем содержимое QPixmap в объекте QLabel
            self.image.setPixmap(self.pixmap)

    def search(self):
        print('я работаю!')


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": mp.ll(),
        "spn": ",".join([str(mp.zoom), str(mp.zoom)]),
        "l": mp.type
    }
    response = requests.get(map_request, params=params)
    print(response)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def main():
    app = QApplication(sys.argv)
    ex = WindowMain()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
