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
        
        self.leitor_ritmos.canvas.tempo_data.update_duration(self.metronome.slider.value())
        
        layout.addWidget(self.metronome)
        layout.addWidget(self.leitor_ritmos)

        # Define o layout na janela
        self.setLayout(layout)
        
        self.metronome.bpm_alterado.connect(self.leitor_ritmos.atualizar_bpm)
        self.metronome.clique_ocorreu.connect(self.leitor_ritmos.proximo_tempo)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MeuApp()
    
    janela.leitor_ritmos.canvas.carregar_json("./ritmos/cancao1.json")
    
    janela.show()
    
    
    sys.exit(app.exec_())
