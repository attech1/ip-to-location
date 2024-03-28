import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class IPGeolocationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('IP Location Tool')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.ip_label = QLabel('Enter IP Address:')
        layout.addWidget(self.ip_label)

        self.ip_input = QLineEdit()
        layout.addWidget(self.ip_input)

        self.location_label = QLabel()
        layout.addWidget(self.location_label)

        self.locate_button = QPushButton('Locate IP')
        self.locate_button.clicked.connect(self.get_location)
        layout.addWidget(self.locate_button)

        self.setLayout(layout)

    def get_location(self):
        ip_address = self.ip_input.text()
        if ip_address:
            try:
                response = requests.get(f'http://ip-api.com/json/{ip_address}')
                data = response.json()
                if data['status'] == 'success':
                    country = data['country']
                    city = data['city']
                    self.location_label.setText(f'Location: {city}, {country}')
                else:
                    self.location_label.setText('Location not found')
            except Exception as e:
                print(f'Error: {e}')
        else:
            self.location_label.setText('Please enter an IP address')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IPGeolocationApp()
    window.show()
    sys.exit(app.exec_())
