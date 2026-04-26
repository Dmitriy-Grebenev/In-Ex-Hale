import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QTimer

START_RADIUS = 45
END_RADIUS = 95
UPDATE_RATE = 50  # ms

class BreathingCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setMinimumSize(200, 200)

        # Animation properties
        self.current_radius = START_RADIUS
        self.states = ("INHALE", "HOLD", "EXHALE")
        self.current_state = self.states[0]  # INHALE
        self.index = 0

        # Timing parameters (seconds)
        self.inhale_duration = 4   # 4 seconds
        self.hold_duration = 7     # 7 seconds
        self.exhale_duration = 8   # 8 seconds (исправлено)

        self.current_duration = self.inhale_duration
        self.animation_step = self.calculate_animation_step()

        # Timers
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_circle)

        self.hold_timer = QTimer()
        self.hold_timer.setSingleShot(True)
        self.hold_timer.timeout.connect(self.end_hold)

    def start_animation(self):
        """Сброс и запуск дыхательного цикла"""
        self.reset_state()
        self.animation_timer.start(UPDATE_RATE)

    def stop_animation(self):
        """Остановка анимации и сброс радиуса"""
        self.animation_timer.stop()
        self.hold_timer.stop()
        self.current_radius = START_RADIUS
        self.update()

    def reset_state(self):
        """Сброс всех параметров в начальное состояние (INHALE)"""
        self.current_state = "INHALE"
        self.current_radius = START_RADIUS
        self.current_duration = self.inhale_duration
        self.animation_step = self.calculate_animation_step()
        self.hold_timer.stop()
        self.update()

    def animate_circle(self):
        """Изменение радиуса в зависимости от текущего состояния"""
        if self.current_state == "INHALE":
            self.current_radius += self.animation_step
            if self.current_radius >= END_RADIUS:
                self.current_radius = END_RADIUS
                # Переход в режим удержания
                self.current_state = "HOLD"
                self.hold_timer.start(int(self.hold_duration * 1000))
        elif self.current_state == "EXHALE":
            self.current_radius -= self.animation_step
            if self.current_radius <= START_RADIUS:
                self.current_radius = START_RADIUS
                # Переход обратно на вдох
                self.current_state = "INHALE"
                self.current_duration = self.inhale_duration
                self.animation_step = self.calculate_animation_step()
        # Для HOLD радиус не меняется – только перерисовка

        self.update()

    def end_hold(self):
        """Вызывается по окончании времени удержания – переключает на выдох"""
        if self.current_state == "HOLD":
            self.current_state = "EXHALE"
            self.current_duration = self.exhale_duration
            self.animation_step = self.calculate_animation_step()

    def paintEvent(self, event):
        """Отрисовка круга и текста"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(30, 30, 46))

        center_x = self.width() // 2
        center_y = self.height() // 2

        # Цвет в зависимости от состояния
        if self.current_state == "INHALE":
            color = QColor(128, 0, 128)
        elif self.current_state == "EXHALE":
            color = QColor(0, 206, 209)
        else:  # HOLD
            color = QColor(79, 175, 0)

        painter.setBrush(QColor(color.red(), color.green(), color.blue(), 80))
        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)

        rect = QRectF(
            center_x - self.current_radius,
            center_y - self.current_radius,
            2 * self.current_radius,
            2 * self.current_radius
        )
        painter.drawEllipse(rect)

        painter.setPen(QColor(200, 200, 255))
        font = QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)

        text_rect = QRectF(center_x - 50, center_y - 20, 100, 40)
        painter.drawText(text_rect, Qt.AlignCenter, self.current_state)

    def sizeHint(self):
        return self.minimumSize()

    def calculate_animation_step(self):
        """Вычисляет шаг изменения радиуса за один тик таймера (UPDATE_RATE)"""
        total_steps = self.current_duration * (1000 / UPDATE_RATE)
        return (END_RADIUS - START_RADIUS) / total_steps