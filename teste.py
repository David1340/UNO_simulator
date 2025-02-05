from UNO import JogoUNO

Jogadores = ["David","Nilson","Elyson"]
contagem  = [0,0,0]
for _ in range(10000):
    jogo = JogoUNO(Jogadores)
    vencedor = jogo.iniciar_jogo()
    #print(vencedor)
    index = Jogadores.index(vencedor)
    contagem[index] = contagem[index] + 1

print(contagem) 