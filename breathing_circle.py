import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt

START_RADIUS = 45
END_RADIUS = 95
UPDATE_RATE = 50 # ms

class BreathingCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setMinimumSize(200, 200)
        
        # Animation properties
        self.current_radius = START_RADIUS #100
        self.states = ("INHALE", "HOLD", "EXHALE")
        
        self.is_inhaling = True
    
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_circle)
        
        # Timing parameters (in milliseconds)
        self.inhale_duration = 4  # 4 seconds
        self.hold_duration = 7 # 7 seconds (in future addons)
        self.exhale_duration = 4  # 8 seconds

        self.current_duration = self.inhale_duration
        
        # Animation properties
        self.animation_step = self.calculate_animation_step()

        self.animation_direction = 1.0  # 1 for inhale, -1 for exhale
        
    def start_animation(self):
        """Start the breathing animation"""
        self.animation_timer.start(UPDATE_RATE)  # Update every 100ms
        
    def stop_animation(self):
        """Stop the breathing animation"""
        self.animation_timer.stop()
        self.current_radius = START_RADIUS
        self.update()  # Redraw to reset circle
        
    def animate_circle(self):
        """Animate the circle size for breathing"""
        # Calculate new radius based on animation direction
        if self.is_inhaling:
            self.current_radius += self.animation_step
            if self.current_radius >= END_RADIUS:  # Max radius
                self.is_inhaling = False
                self.current_duration = self.exhale_duration
                self.animation_step = self.calculate_animation_step()
                self.animation_direction = -1
        else:
            self.current_radius -= self.animation_step
            if self.current_radius <= START_RADIUS:  # Min radius
                self.is_inhaling = True
                self.current_duration = self.inhale_duration
                self.animation_step = self.calculate_animation_step()
                self.animation_direction = 1
                
        self.update()  # Trigger repaint
        
    def paintEvent(self, event):
        """Draw the breathing circle"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw transparent background
        painter.fillRect(self.rect(), QColor(30, 30, 46))
        
        # Calculate center and radius
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # Draw circle with gradient effect
        color = QColor(128, 0, 128) if self.is_inhaling else QColor(0, 206, 209)
        
        # Create a semi-transparent fill
        painter.setBrush(QColor(color.red(), color.green(), color.blue(), 80))
        
        # Draw the circle with outline
        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)
        
        # Draw the circle
        rect = QRectF(
            center_x - self.current_radius,
            center_y - self.current_radius,
            2 * self.current_radius,
            2 * self.current_radius
        )
        painter.drawEllipse(rect)
        
        # Draw text indicating breath direction
        painter.setPen(QColor(200, 200, 255))
        font = QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        
        text = "INHALE" if self.is_inhaling else "EXHALE"
        
        # INHALE in coming update
        # if self.is_inhaling:
        #     text = "INHALE"
        
        text_rect = QRectF(
            center_x - 50,
            center_y - 20,
            100,
            40
        )
        painter.drawText(text_rect, Qt.AlignCenter, text)
        
    def sizeHint(self):
        return self.minimumSize()

    def calculate_animation_step(self):
        return (END_RADIUS - START_RADIUS) / (self.current_duration * (1000 / UPDATE_RATE))
