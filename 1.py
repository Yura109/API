import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from requests import get


class StaticYandexMap:
    def __init__(self, longitude, latitude, map_type='map'):
        self.params = {
            'll': f'{longitude},{latitude}',
            'l': map_type,
            'z': 10,
        }

    def get_url(self):
        url = 'https://static-maps.yandex.ru/1.x/'
        return f"{url}?{'&'.join([f'{k}={val}' for k, val in self.params.items()])}"


class MapWindow(QMainWindow):
    def __init__(self, api, coordinates, zoom, parent=None):
        super().__init__(parent)
        self.api = api
        self.coordinates = coordinates
        self.zoom = zoom
        self.image = None
        self.create_ui()
        self.load_map()

    def create_ui(self):
        self.setWindowTitle("Карта")
        self.setGeometry(300, 300, 550, 350)
        coordinates_label = QLabel("Введите координаты:")
        self.coordinates_input = QLineEdit()
        update_button = QPushButton("Обновить карту")
        update_button.clicked.connect(self.update_map)
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.map_label = QLabel()
        layout.addWidget(coordinates_label)
        layout.addWidget(self.coordinates_input)
        layout.addWidget(update_button)
        layout.addWidget(self.map_label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_map(self):
        static_map = StaticYandexMap(*map(float, self.coordinates.split(',')))
        static_map.params['z'] = self.zoom
        url = static_map.get_url()
        response = get(url)
        if response.status_code == 200:
            with open("map_temp.jpg", "wb") as file:
                file.write(response.content)
            self.image = QPixmap("map_temp.jpg")
            self.map_label.setPixmap(self.image)
            self.map_label.setFocus()
        else:
            self.map_label.setText('Ошибка загрузки карты')

    def update_map(self):
        self.coordinates = self.coordinates_input.text()
        self.load_map()




if __name__ == '__main__':
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    coordinates = "37.620070,55.753630"
    zoom = 10
    app = QApplication(sys.argv)
    window = MapWindow(apikey, coordinates, zoom)
    window.show()
    sys.exit(app.exec_())