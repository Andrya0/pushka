import pygame, requests, sys, os
from PyQt5 import Qt


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

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
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
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()