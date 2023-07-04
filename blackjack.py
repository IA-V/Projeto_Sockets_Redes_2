import random

# Definindo as cartas e seus valores
baralho = [
    'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
]
valores_cartas = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10
}

# Classe para representar uma mão de cartas
class Mao:
    def __init__(self):
        self.cartas = []

    def receber_carta(self, carta):
        self.cartas.append(carta)

    def calcular_pontos(self):
        total = sum([valores_cartas[carta] for carta in self.cartas])
        # Verifica se há um Ás na mão e se contar como 11 não ultrapassa 21 pontos
        if 'A' in self.cartas and total + 10 <= 21:
            total += 10
        return total

# Função para iniciar um novo jogo
def novo_jogo():
    # Inicializando as mãos dos jogadores e do dealer
    server_hand = Mao()

    for client in client_sockets:
        client
    client_hand = Mao()

    # Distribuindo duas cartas para cada jogador
    for _ in range(2):
        client_hand.receber_carta(random.choice(baralho))
        server_hand.receber_carta(random.choice(baralho))

    # Loop do jogo
    while True:
        # Mostra as cartas do jogador e a primeira carta do dealer
        print("Sua mão:", client_hand.cartas)
        print("Pontuação:", client_hand.calcular_pontos())
        print("Dealer mostra:", server_hand.cartas[0])

        # Verifica se o jogador já estourou 21 pontos
        if client_hand.calcular_pontos() > 21:
            print("Você estourou 21 pontos! Você perdeu.")
            break

        # Pergunta ao jogador se ele deseja receber mais uma carta ou parar
        escolha = input("Deseja [M]ais uma carta ou quer [P]arar? ").lower()
        if escolha == 'm':
            client_hand.receber_carta(random.choice(baralho))
        else:
            # Jogador parou, agora é a vez do dealer
            # Dealer recebe mais cartas até atingir pelo menos 17 pontos
            while server_hand.calcular_pontos() < 17:
                server_hand.receber_carta(random.choice(baralho))
            
            # Mostra as mãos do jogador e do dealer
            print("\n--- Fim do jogo ---")
            print("Sua mão:", client_hand.cartas)
            print("Pontuação:", client_hand.calcular_pontos())
            print("Mão do dealer:", server_hand.cartas)
            print("Pontuação do dealer:", server_hand.calcular_pontos())

            # Verifica o resultado do jogo
            pontos_jogador = client_hand.calcular_pontos()
            pontos_dealer = server_hand.calcular_pontos()
            if pontos_jogador > pontos_dealer:
                print("Você venceu!")
            elif pontos_jogador < pontos_dealer:
                print("Você perdeu!")
            else:
                print("Empate!")

            break

# Inicia o jogo
# novo_jogo()