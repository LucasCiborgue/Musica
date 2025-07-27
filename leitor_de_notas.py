"""

Nota -----------	Nome --------	Valor
Semibreve   	whole note	        4.0
Mínima	        half note	        2.0
Semínima	    quarter note	    1.0
Colcheia	    eighth note	        0.5
Semicolcheia	sixteenth note	    0.25
Fusa	        32nd note	        0.125
Semifusa	    64th note	        0.0625

"""

from utilities import *

class SequenciaNotas:
    def __init__(self, notas):
        self.notas = notas  # lista de dicts { "nota": "colcheia", "valor": 0.5 }

    def get_imagens(self):
        imagens = []
        for nota in self.notas:
            nome_arquivo = f"./recursos/notas/{nota['nota']}.png"
            if os.path.exists(nome_arquivo):
                img = QPixmap(nome_arquivo).scaledToHeight(40, Qt.SmoothTransformation)
                imagens.append(img)
        return imagens

class CanvasNotas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.sequencias = []
        self.index_atual = 0
        self.index_nota = 0  # índice da nota atual sendo clicada
        self.nome_musica = ""

    def carregar_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        self.sequencias = [SequenciaNotas(seq) for seq in dados["ritmos"]]
        self.index_atual = 0
        self.index_nota = 0
        self.nome_musica = os.path.basename(path)
        self.update()

    def registrar_batida(self):
        if not self.sequencias:
            return

        if self.index_atual == (len(self.sequencias)):
            self.index_atual = 0
            self.index_nota = 0
            self.update()
            return
            
        notas = self.sequencias[self.index_atual].notas
        self.index_nota += 1
        if self.index_nota > len(notas):
            self.index_atual += 1
            self.index_nota = 0
        self.update()

    def paintEvent(self, event):
        if not self.sequencias:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        largura = self.width()
        y_positions = [50, 140, 230]
        
        if(self.index_atual == (len(self.sequencias))):
            indices = [self.index_atual - 1, self.index_atual, 0]
        else:
            indices = [self.index_atual - 1, self.index_atual, self.index_atual + 1]

        for pos, idx in zip(y_positions, indices):
            if 0 <= idx < len(self.sequencias):
                notas = self.sequencias[idx].notas
                x = (largura - (len(notas) * 50 + (len(notas) - 1) * 10)) // 2
                for i, nota in enumerate(notas):
                    img_path = f"./recursos/notas/{nota['nota']}.png"
                    if os.path.exists(img_path):
                        img = QPixmap(img_path).scaledToHeight(40, Qt.SmoothTransformation)
                        if idx == self.index_atual and i < self.index_nota:
                            painter.fillRect(x - 2, pos - 2, img.width() + 4, img.height() + 4, Qt.blue)
                        painter.drawPixmap(x, pos, img)
                        x += img.width() + 10


class LeitorDeRitmos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leitor de Ritmos")

        layout_principal = QHBoxLayout()
        layout_esquerda = QVBoxLayout()
        layout_direita = QVBoxLayout()

        # === Canvas Central ===
        self.canvas = CanvasNotas()
        layout_direita.addWidget(self.canvas)

        # === Caixa: música: nome.json ===
        self.grupo_musica = QGroupBox("música: nenhum arquivo")
        layout_grupo = QVBoxLayout()

        # Botão BEAT
        self.btn_beat = QPushButton("BEAT")
        self.btn_beat.setMinimumSize(150, 150)
        self.btn_beat.clicked.connect(self.bater)
        layout_grupo.addWidget(self.btn_beat)

        # Botão PRÓXIMA SEQUÊNCIA (opcional)
        self.btn_proximo = QPushButton("Próximo Tempo")
        self.btn_proximo.clicked.connect(self.proximo_tempo)
        layout_grupo.addWidget(self.btn_proximo)

        self.grupo_musica.setLayout(layout_grupo)
        layout_esquerda.addWidget(self.grupo_musica)
        layout_esquerda.addStretch()

        # === Botão carregar JSON ===
        self.btn_carregar = QPushButton("Carregar JSON")
        self.btn_carregar.clicked.connect(self.carregar_arquivo)
        layout_direita.addWidget(self.btn_carregar)

        # === Organizar layouts ===
        layout_principal.addLayout(layout_esquerda)
        layout_principal.addLayout(layout_direita)
        self.setLayout(layout_principal)

    def carregar_arquivo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar JSON", "", "Arquivos JSON (*.json)")
        if path:
            self.canvas.carregar_json(path)
            self.grupo_musica.setTitle("música: " + os.path.basename(path))

    def bater(self):
        self.canvas.registrar_batida()

    def proximo_tempo(self):
        if self.canvas.index_atual < len(self.canvas.sequencias) - 1:
            self.canvas.index_atual += 1
            self.canvas.index_nota = 0
            self.canvas.update()
        else:
            self.canvas.index_atual = 0
            self.canvas.index_nota = 0
            self.canvas.update()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LeitorDeRitmos()
    win.resize(600, 400)
    win.show()
    sys.exit(app.exec_())
