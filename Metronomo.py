from utilities import *



class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.metronomo_pixmap = QPixmap(os.path.join('recursos', 'metronomo.png')).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ponteiro_pixmap = QPixmap(os.path.join('recursos', 'ponteiro_m.png')).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.ponteiro_angle = -30  # Inicia inclinado para a esquerda
        self.pivot_x = 150  # ponto fixo X (ajuste conforme necessário)
        self.pivot_y = 225   # ponto fixo Y (ajuste conforme necessário)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        # Desenhar metronomo
        mx = (self.width() - self.metronomo_pixmap.width()) // 2
        my = (self.height() - self.metronomo_pixmap.height()) // 2
        painter.drawPixmap(mx, my, self.metronomo_pixmap)

        # Desenhar ponteiro rotacionado ao redor da BASE (parte inferior)
        painter.save()
        painter.translate(self.pivot_x, self.pivot_y)
        painter.rotate(self.ponteiro_angle)

        pw = self.ponteiro_pixmap.width()
        ph = self.ponteiro_pixmap.height()

        # Aqui o ponteiro é desenhado com a base no pivô
        painter.drawPixmap(-pw // 2, -ph, self.ponteiro_pixmap)
        painter.restore()

        # Desenhar bolinha vermelha no ponto de pivô
        painter.setBrush(Qt.red)
        painter.setPen(Qt.NoPen)
        radius = 6
        painter.drawEllipse(self.pivot_x - radius, self.pivot_y - radius, radius * 2, radius * 2)

        
    # Propriedade animável do ângulo
    def get_angle(self):
        return self.ponteiro_angle
        
    def set_angle(self, angle):
        self.ponteiro_angle = angle
        self.update()
        
    angle = pyqtProperty(float, get_angle, set_angle)


class MetronomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Metrônomo Animado')
        self.resize(500, 300)

        layout = QHBoxLayout(self)

        # Canvas
        self.canvas = Canvas()
        layout.addWidget(self.canvas)

        # Side Frame
        side_frame = QVBoxLayout()

        self.label_tempo = QLabel("Andante (76 BPM)", self)
        self.label_tempo.setAlignment(Qt.AlignCenter)
        side_frame.addWidget(self.label_tempo)

        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(40)
        self.slider.setMaximum(200)
        self.slider.setValue(76)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.update_tempo)
        side_frame.addWidget(self.slider)

        """
        # Controle de Pivot X
        self.pivot_x_box = QSpinBox()
        self.pivot_x_box.setRange(-300, 300)
        self.pivot_x_box.setValue(self.canvas.pivot_x)
        self.pivot_x_box.setPrefix("Pivot X: ")
        self.pivot_x_box.valueChanged.connect(self.update_pivot)
        side_frame.addWidget(self.pivot_x_box)

        # Controle de Pivot Y
        self.pivot_y_box = QSpinBox()
        self.pivot_y_box.setRange(-300, 300)
        self.pivot_y_box.setValue(self.canvas.pivot_y)
        self.pivot_y_box.setPrefix("Pivot Y: ")
        self.pivot_y_box.valueChanged.connect(self.update_pivot)
        side_frame.addWidget(self.pivot_y_box)
        #"""


        layout.addLayout(side_frame)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        
        # Animação
        self.angle_state = -30
        self.animation = QPropertyAnimation(self.canvas, b"angle")
        self.animation.setDuration(200)  # será ajustado dinamicamente

        self.update_tempo(self.slider.value())
        self.timer.start()

    def update_pivot(self):
        self.canvas.pivot_x = self.pivot_x_box.value()
        self.canvas.pivot_y = self.pivot_y_box.value()
        self.canvas.update()

    def update_tempo(self, bpm):
        nome = self.bpm_to_nome(bpm)
        self.label_tempo.setText(f"{nome} ({bpm} BPM)")

        interval_ms = int(60000 / bpm)
        self.timer.setInterval(interval_ms)
        self.animation.setDuration(interval_ms // 2)

    def tick(self):
        self.play_click()

        # Alternar ângulo e animar suavemente
        start = self.canvas.angle
        end = 30 if self.angle_state == -30 else -30
        self.angle_state = end

        self.animation.stop()
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()


    def play_click(self):
        bpm = self.slider.value()
        speed = bpm / 76  # Andante = referência
        speed = max(0.5, min(2.0, speed))

        subprocess.Popen([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel", "quiet",
            "-af", f"atempo={speed:.2f}",
            os.path.join("recursos", "click.wav")
        ])

    def bpm_to_nome(self, bpm):
        if bpm < 60:
            return "Largo"
        elif bpm < 76:
            return "Adagio"
        elif bpm < 108:
            return "Andante"
        elif bpm < 120:
            return "Moderato"
        elif bpm < 168:
            return "Allegro"
        else:
            return "Presto"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetronomeApp()
    window.show()
    sys.exit(app.exec_())