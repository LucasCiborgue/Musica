from utilities import *
from leitor_de_notas import *
from Metronomo import *

class MeuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemplo com QVBoxLayout")

        # Layout vertical
        layout = QVBoxLayout()

        # Adiciona ao layout
        self.metronome = MetronomeApp()
        self.leitor_ritmos = LeitorDeRitmos()
        
        layout.addWidget(self.metronome)
        layout.addWidget(self.leitor_ritmos)

        # Define o layout na janela
        self.setLayout(layout)
        
        self.metronome.clique_ocorreu.connect(self.leitor_ritmos.proximo_tempo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MeuApp()
    janela.show()
    sys.exit(app.exec_())
