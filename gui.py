import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

import flightdata
import mapgenerator


class MapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Viewer")
        self.browser = QWebEngineView()
        self.initUI()
        self.resize(1600, 800)

    def initUI(self):
        # Load the initial map
        self.load_map("world_map.html")

        # Right-hand side controls layout
        right_layout = QVBoxLayout()

        # Button for toggling maps
        home_button = QPushButton('Home View')
        home_button.clicked.connect(self.home_view)
        home_button.setFixedSize(100, 30)  # Set fixed size for the button
        right_layout.addWidget(home_button)

        # User input textboxes
        self.user_input1 = QLineEdit()
        self.user_input1.setPlaceholderText("Departure(IATA Code):")
        self.user_input2 = QLineEdit()
        self.user_input2.setPlaceholderText("Arrival(IATA Code):")
        right_layout.addWidget(self.user_input1)
        right_layout.addWidget(self.user_input2)

        # Submit button
        submit_button = QPushButton('Add Journey')
        submit_button.clicked.connect(self.add_journey)
        right_layout.addWidget(submit_button)

        # Feedback label
        self.feedback_label = QLabel('')
        right_layout.addWidget(self.feedback_label)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.browser, 75)
        main_layout.addLayout(right_layout, 15)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_map(self, map_name):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, map_name)
        self.browser.load(QUrl.fromLocalFile(file_path))

    def home_view(self):
        current_url = self.browser.url().toString()
        self.load_map(current_url[7:])

    def add_journey(self):
        # Check if the textboxes are filled
        if self.user_input1.text() and self.user_input2.text():
            departure = self.user_input1.text()
            arrival = self.user_input2.text()
            flightdata.add_journey(departure, arrival)
            location_list = flightdata.read_journey('airport_pairs.csv')
            mapgenerator.map_generation(location_list)
            self.home_view()
            self.feedback_label.setText("Information captured successfully.")
        else:
            self.feedback_label.setText("Please fill in all textboxes.")

def display():
    app = QApplication(sys.argv)
    window = MapViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    display()
