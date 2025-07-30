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

class TempoData:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.progress = 0
        self.duration_secs = 0
        self.duration_ms = 0
        self.start_time = self.current_millis()
        self.update_duration(bpm)
        

    def current_millis(self):
        return int(time.time() * 1000)

    def get_current_time(self):
        return self.current_millis() - self.start_time
        
    def update_duration(self, bpm=120):
        self.bpm = bpm
        self.start_time = self.current_millis()
        self.duration_ms = 60000 / self.bpm  # tempo para percorrer a linha (em ms)
        self.duration_secs =  self.bpm/60

    def update_progress(self):
        elapsed = self.current_millis() - self.start_time
        self.progress = (elapsed % self.duration_ms) / self.duration_ms

class TempoDisplay(QWidget):
    def __init__(self, tempo_data, parent=None):
        super().__init__(parent)
        
        self.tempo_data = tempo_data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.update_duration(self.tempo_data.bpm)       
        
    def update_duration(self, bpm=120):
        self.tempo_data.update_duration(bpm)
        
        self.line_x = 0
        
        self.timer.start(16)  # aproximadamente 60 FPS

    def update_position(self):
        self.tempo_data.update_progress()
        self.line_x = int(self.tempo_data.progress * self.width())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

        pen = QPen(Qt.red, 3)
        painter.setPen(pen)

        painter.drawLine(self.line_x, 0, self.line_x, self.height())

class CanvasNotas(QWidget):
    def __init__(self, tempo_data):
        super().__init__()
        self.setMinimumSize(400, 300)        
        self.sequencias = []
        self.index_atual = 0
        self.index_nota = 0  # índice da nota atual sendo clicada
        self.nome_musica = ""
        
        self.tempo_sequencia = 0
 
        self.tempo_data = tempo_data
        
        self.tempos_sequencia = []
        self.tempos_entre_notas = []
        
        self.TEMPO_BATIDA = 0.25

    def carregar_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        self.sequencias = [SequenciaNotas(seq) for seq in dados["ritmos"]]
        
        self.resetTempo()
        
        self.nome_musica = os.path.basename(path)
        
        self.criar_sequencia_tempo_nota()
        
        self.update()
    
    def reset_index_nota(self):
        self.index_atual = 0
        self.index_nota = 0

    def resetTempo(self):
        self.tempo_sequencia = 0

    def registrar_batida(self):
        if not self.sequencias:
            return

        if self.index_atual == (len(self.sequencias)):
            self.reset_index_nota()
            self.resetTempo()           
            self.update()
            return
        
        notas = self.sequencias[self.index_atual].notas
        tam = len(notas)
        
        if self.index_nota > tam:
            self.index_atual += 1
            self.index_nota = 0
            
            self.resetTempo()
        else:
            
            self.tempo_sequencia = self.tempo_data.progress
            i = self.index_nota
            while i < tam:
                if self.tempo_sequencia < self.tempos_entre_notas[i]:
                    desvio = abs(self.tempo_sequencia - self.tempos_sequencia[i])
                                
                    print("================================")
                    print("tempo esp: ",self.tempos_sequencia[i])
                    print("desvio: ",desvio)
                
                
                    if desvio < 0.1:  # exato (por exemplo, menos de 50ms)
                        cor = QColor("blue")
                    elif desvio < 0.2:
                        cor = QColor("green")
                    else:
                        cor = QColor("yellow")
                    
                    self.cores[i] = cor
                
                i+=1
            self.index_nota += 1

        self.update()
    
    #"""
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

                                
                            #"""
                            
                            
                            painter.fillRect(x - 2, pos - 2, img.width() + 4, img.height() + 4, self.cores[i])
                            
                            #painter.fillRect(x - 2, pos - 2, img.width() + 4, img.height() + 4, Qt.blue)
                        painter.drawPixmap(x, pos, img)
                        x += img.width() + 10
          
        #"""  
        if (self.index_atual < (len(self.sequencias))):
            largura = self.width()
            altura = self.height()
            y_linha = altura // 2

            # Desenha linha base
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(20, y_linha, largura - 20, y_linha)

            sequencia = self.sequencias[self.index_atual]
            
            # Calcula posições das elipses para cada nota
            x_inicio = 20
            x_fim = largura - 20
            largura_linha = x_fim - x_inicio

            i = 0
            for nota in sequencia.notas:
                if i < len(self.tempos_sequencia):
                    pos_relativa = self.tempos_sequencia[i]  # entre 0 e 1
                    x_pos = x_inicio + pos_relativa * largura_linha

                    # Desenha elipse da nota
                    painter.setBrush(Qt.blue)
                    raio = 8
                    painter.drawEllipse(int(x_pos - raio), int(y_linha - raio), int(raio*2), int(raio*2))
                    i += 1

        #print("largura da linha",largura_linha)
        
        """
        # Desenha marcador do tempo atual
        # Assume self.tempo_decorrido é o tempo dentro da sequência em segundos   
        
        tempo = self.tempo_sequencia - self.tempo_inicial

        #tempo_atual_rel = min( (tempo)/ (duracao_total * self.bpm), 1.0)  # normaliza 0-1
        tempo_atual_rel = min( (tempo), 1.0)  # normaliza 0-1
        
        x_tempo = x_inicio + tempo_atual_rel * largura_linha

        painter.setPen(QPen(Qt.red, 3))
        painter.drawLine(int(x_tempo), int(y_linha - 20), int(x_tempo), int(y_linha + 20))
    #"""
        
    def criar_sequencia_tempo_nota(self):
        sequencia = self.sequencias[self.index_atual]
        tempo_acumulado = 0
        
        self.tempos_sequencia = []
        self.tempos_entre_notas = []
        self.cores = []
        
        
        for nota in sequencia.notas:
            tempox = nota.get("valor", 1.0)*2*self.TEMPO_BATIDA
            tempo_acumulado += tempox
            self.tempos_sequencia.append(tempo_acumulado)
            tempo_acumulado += tempox
            self.tempos_entre_notas.append(tempo_acumulado)
            self.cores.append(Qt.gray)
        
        
        print("tempos_sequencia; ", self.tempos_sequencia)


class LeitorDeRitmos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leitor de Ritmos")

        layout_principal = QHBoxLayout()
        layout_esquerda = QVBoxLayout()
        layout_direita = QVBoxLayout()

        # === Canvas Central ===
        self.tempo_data = TempoData()
        self.canvas = CanvasNotas(self.tempo_data)
        self.tempo_display = TempoDisplay(self.tempo_data)
        self.tempo_display.setMinimumHeight(66)
        
        
        layout_direita.addWidget(self.tempo_display)
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
        self.canvas.resetTempo()
        self.canvas.index_nota = 0
        
        if self.canvas.index_atual < len(self.canvas.sequencias) - 1:
            self.canvas.index_atual += 1
            self.canvas.criar_sequencia_tempo_nota()            
            self.canvas.update()
        else:
            self.canvas.index_atual = 0            
            self.canvas.tempo_inicial_esperados = time.time()
            self.canvas.criar_sequencia_tempo_nota()
            self.canvas.update()
            
    def atualizar_bpm(self, novo_bpm):
        self.tempo_display.update_duration(novo_bpm)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LeitorDeRitmos()
    win.resize(600, 400)
    win.show()
    sys.exit(app.exec_())
