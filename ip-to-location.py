import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QHBoxLayout
from PyQt5.QtCore import QTranslator


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.language_label = QLabel('Select Language:')
        layout.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(['English', 'German', 'French', 'Dutch'])
        layout.addWidget(self.language_combo)

        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)
        buttons_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def save_settings(self):
        selected_language = self.language_combo.currentText()
        self.parent().change_language(selected_language)
        self.close()


class IPGeolocationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('IP Location Tool')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.ip_label = QLabel()
        layout.addWidget(self.ip_label)

        self.ip_input = QLineEdit()
        layout.addWidget(self.ip_input)

        self.location_label = QLabel()
        layout.addWidget(self.location_label)

        self.locate_button = QPushButton()
        self.locate_button.clicked.connect(self.get_location)
        layout.addWidget(self.locate_button)

        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        self.setLayout(layout)

        self.translator = QTranslator()
        self.load_language('English')

    def load_language(self, language):
        if language == 'German':
            self.translator.load('translations/ip_location_app_de')
        elif language == 'French':
            self.translator.load('translations/ip_location_app_fr')
        elif language == 'Dutch':
            self.translator.load('translations/ip_location_app_nl')
        else:
            self.translator.load('translations/ip_location_app_en')

        QApplication.instance().installTranslator(self.translator)
        self.update_ui_texts()

    def update_ui_texts(self):
        self.ip_label.setText(self.tr('Enter IP Address:'))
        self.location_label.setText(self.tr('Location:'))
        self.locate_button.setText(self.tr('Locate IP'))
        self.settings_button.setText(self.tr('Settings'))

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def change_language(self, language):
        self.load_language(language)

    def get_location(self):
        ip_address = self.ip_input.text()
        if ip_address:
            try:
                response = requests.get(f'http://ip-api.com/json/{ip_address}')
                data = response.json()
                if data['status'] == 'success':
                    country = data['country']
                    city = data['city']
                    self.location_label.setText(self.tr(f'Location: {city}, {country}'))
                else:
                    self.location_label.setText(self.tr('Location not found'))
            except Exception as e:
                print(f'Error: {e}')
        else:
            self.location_label.setText(self.tr('Please enter an IP address'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IPGeolocationApp()
    window.show()
    sys.exit(app.exec_())
