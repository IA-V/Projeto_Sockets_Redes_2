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