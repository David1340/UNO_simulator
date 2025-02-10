from UNO import JogoUNO, CartaUNO

Jogadores = ["David", "Nilson"]

# Configuração específica das mãos dos jogadores
maos_iniciais = [
    [CartaUNO("vermelho", "+2"), CartaUNO("azul", "3")],
    [CartaUNO("verde", "+2"), CartaUNO("amarelo", "bloqueio")]
]

# Primeira carta jogada no montante
primeira_carta = CartaUNO("vermelho", "3")

jogo = JogoUNO(Jogadores, maos_iniciais, primeira_carta)
vencedor = jogo.iniciar_jogo()