import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from breathing_circle import BreathingCircle
from timer_widget import TimerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("In-Ex-Hale")
        self.setFixedSize(600, 500)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create breathing circle
        self.breathing_circle = BreathingCircle()
        layout.addWidget(self.breathing_circle)
        
        # Create timer widget
        self.timer_widget = TimerWidget()
        layout.addWidget(self.timer_widget)
        
        # Create start/stop button
        self.start_stop_button = QPushButton("Start Joyrney")
        self.start_stop_button.setFixedHeight(50)
        self.start_stop_button.clicked.connect(self.toggle_meditation)
        layout.addWidget(self.start_stop_button)
        
        # Initialize meditation state
        self.meditation_active = False
        
        # Apply styles
        self.apply_styles()
        
    def toggle_meditation(self):
        if not self.meditation_active:
            self.breathing_circle.start_animation()
            self.timer_widget.start_timer()
            self.start_stop_button.setText("Stop Journey")
        else:
            self.breathing_circle.stop_animation()
            self.timer_widget.stop_timer()
            self.start_stop_button.setText("Start Journey")
            
        self.meditation_active = not self.meditation_active
        
    def apply_styles(self):
        # Load and apply CSS styles
        with open('styles.qss', 'r') as file:
            style_sheet = file.read()
            self.setStyleSheet(style_sheet)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
