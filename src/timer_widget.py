import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(80)
        
        # Create layout and label
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("color: #a0a0ff; font-size: 24px;")
        self.time_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(20)
        self.time_label.setFont(font)
        
        layout.addWidget(self.time_label)
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.meditation_time = QTime(0, 0, 0)
        self.is_running = False
        
    def start_timer(self):
        """Start the meditation timer"""
        self.reset_timer()
        if not self.is_running:
            self.timer.start(1000)  # Update every second
            self.is_running = True
            
    def stop_timer(self):
        """Stop the meditation timer"""
        self.timer.stop()
        self.is_running = False
        
    def update_time(self):
        """Update the timer display"""
        if self.is_running:
            self.meditation_time = self.meditation_time.addSecs(1)
            time_string = self.meditation_time.toString("mm:ss")
            self.time_label.setText(time_string)
            
    def reset_timer(self):
        """Reset the timer to zero"""
        self.timer.stop()
        self.is_running = False
        self.meditation_time = QTime(0, 0, 0)
        self.time_label.setText("00:00")
