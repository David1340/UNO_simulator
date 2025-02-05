import random
import time

class CartaUNO:
    CORES = ["vermelho", "azul", "verde", "amarelo"]
    VALORES = [str(i) for i in range(0, 10)] + ["+2", "inverter", "bloqueio"]
    CARTAS_ESPECIAIS = ["coringa", "+4"]

    def __init__(self, cor=None, valor=None):
        if valor in self.CARTAS_ESPECIAIS:
            self.cor = None  # Cartas especiais não possuem cor fixa
            self.valor = valor
        elif cor in self.CORES and valor in self.VALORES:
            self.cor = cor
            self.valor = valor
        else:
            raise ValueError("Carta inválida!")
    
    def __repr__(self):
        return f"{self.cor} {self.valor}" if self.cor else self.valor

class BaralhoUNO:
    def __init__(self):
        self.baralho = self.criar_baralho()
    
    def criar_baralho(self):
        baralho = []
        for cor in CartaUNO.CORES:
            for valor in CartaUNO.VALORES:
                baralho.append(CartaUNO(cor, valor))  # Uma cópia de cada carta
                if valor != "0":
                    baralho.append(CartaUNO(cor, valor))  # Duas cópias para cartas não zero
        for valor in CartaUNO.CARTAS_ESPECIAIS:
            for _ in range(4):
                baralho.append(CartaUNO(None, valor))  # Quatro cartas coringas e +4
        random.shuffle(baralho)
        return baralho
    
    def puxar_carta(self):
        return self.baralho.pop() if self.baralho else None

class JogadorUNO:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []
        self.estrategia = self.estrategia_padrao  # Define estratégia padrão
    
    def comprar_carta(self, baralho):
        carta = baralho.puxar_carta()
        if carta:
            self.mao.append(carta)
    
    def jogar_carta(self, indice):
        if 0 <= indice < len(self.mao):
            return self.mao.pop(indice)
        return None
    
    def estrategia_padrao(self,ultima_carta):
        # Implementação básica: jogar a primeira carta disponível

        for i in range(len(self.mao)):
            if(JogoUNO.carta_permitida(self.mao[i],ultima_carta)):
                return i
            
        return None
    
    def definir_estrategia(self, nova_estrategia):
        self.estrategia = nova_estrategia  # Permite alterar a estratégia dinamicamente

class MontanteUNO:
    def __init__(self):
        self.montante = []
    
    def adicionar_carta(self, carta):
        self.montante.append(carta)
    
    def ultima_carta(self):
        return self.montante[-1] if self.montante else None
    
    def ver_cartas_jogadas(self):
        return self.montante

class JogoUNO:
    def __init__(self, jogadores_nomes):
        self.baralho = BaralhoUNO()
        self.montante = MontanteUNO()
        self.jogadores = [JogadorUNO(nome) for nome in jogadores_nomes]
        self.direcao = 1  # 1 para frente, -1 para trás
        self.jogador_atual = 0
        self.distribuir_cartas()
    
    def distribuir_cartas(self):
        for _ in range(7):  # Cada jogador recebe 7 cartas
            for jogador in self.jogadores:
                jogador.comprar_carta(self.baralho)
    
    def proximo_jogador(self):
        self.jogador_atual = (self.jogador_atual + self.direcao) % len(self.jogadores)
    
    def carta_permitida(carta, ultima):
        #ultima = self.montante.ultima_carta()
        return (carta.cor == ultima.cor or carta.valor == ultima.valor or carta.valor in CartaUNO.CARTAS_ESPECIAIS or ultima.valor in CartaUNO.CARTAS_ESPECIAIS)
    
    def jogar_turno(self):
        #time.sleep(1)
        jogador = self.jogadores[self.jogador_atual]
        indice_carta = jogador.estrategia(self.montante.ultima_carta())
        if indice_carta is not None and indice_carta < len(jogador.mao):
            carta = jogador.mao[indice_carta]
            if JogoUNO.carta_permitida(carta,self.montante.ultima_carta()):
                jogador.jogar_carta(indice_carta)
                self.montante.adicionar_carta(carta)
                #print(f"{jogador.nome} jogou {carta}")
                if(carta.valor == "+2"):
                    self.proximo_jogador()
                    jogador = self.jogadores[self.jogador_atual]
                    for _ in range(2): 
                        jogador.comprar_carta(self.baralho)
                    #print(f"{jogador.nome} comprou duas cartas")
                elif(carta.valor == "+4"):
                    self.proximo_jogador()
                    jogador = self.jogadores[self.jogador_atual]
                    for _ in range(2): 
                        jogador.comprar_carta(self.baralho)
                    #print(f"{jogador.nome} comprou quatro cartas")
                elif(carta.valor == "bloqueio"):
                    self.proximo_jogador()
                    jogador = self.jogadores[self.jogador_atual]
                    #print(f"{jogador.nome} foi bloqueado")
                elif(carta.valor == "inverter"):
                    self.direcao = self.direcao*(-1)

            else:
                #print(f"{jogador.nome} tentou jogar {carta}, mas não pode. Comprou uma carta.")
                jogador.comprar_carta(self.baralho)
        else:
            jogador.comprar_carta(self.baralho)
            #print(f"{jogador.nome} comprou uma carta")
        self.proximo_jogador()
    
    def iniciar_jogo(self):
        self.montante.adicionar_carta(self.baralho.puxar_carta())
        while (all(len(jogador.mao) > 0 for jogador in self.jogadores) and len(self.baralho.baralho) > 0):
            self.jogar_turno()
        vencedor = min(self.jogadores, key=lambda j: len(j.mao))
        #print(f"O vencedor é {vencedor.nome}!")
        return vencedor.nome
