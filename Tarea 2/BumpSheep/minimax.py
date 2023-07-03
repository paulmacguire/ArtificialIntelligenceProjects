import copy
import math
import utils
import random

"""En este archivo se desarrolla el algoritmo minimax."""
# Parte del código fue ayudado por ChatGPT

def minimax(game, depth, alpha=(-math.inf), beta=(math.inf)):
    if depth == 0 or game.blanco.puntaje >= game.objetivo or game.negro.puntaje >= game.objetivo:
        # Función de score
        score = game.blanco.puntaje - game.negro.puntaje

        # Caso fin de recursión
        if depth == 0:
            return ((None, None), score)

        # Casos de término
        if game.blanco.puntaje >= game.objetivo and score > 0:
            return ((None, None), math.inf)  # Gana blanco
        elif game.negro.puntaje >= game.objetivo and score < 0:
            return ((None, None), -math.inf)  # Gana negro
        elif game.negro.puntaje >= game.objetivo and score == 0:
            return ((None, None), 0)  # Empate

    # Se define si se maximiza o minimiza
    maximize = True if game.turno.color == "blanco" else False

    """
    Se deben obtener los posibles movimientos correspondientes a la jugada.
    Los posibles movimientos hay que dejarlos en una lista de tuplas llamada valid_moves.
    valid_moves tendrá elementos del tipo (oveja, fila)
    """
    valid_moves = []

    ovejas_disponibles, filas_disponibles = utils.disponibilidades(game)
    valid_moves = [(oveja, fila) for oveja in ovejas_disponibles for fila in filas_disponibles]

    if maximize:

        score = -math.inf
        best_move = ("0", "0")
        for move in valid_moves:
            # Se hace una copia del juego para simular jugadas sin afectar el juego actual
            game_copy = copy.deepcopy(game)

            # Se realiza la jugada simulada
            utils.ejecutar_jugada(game_copy, move[0], move[1])

            """
            Aplicar el algoritmo en el caso de que se minimice.
            Se tiene que llamar recursivamente a minimax con la profundidad reducida en 1, 
            y comprobar si el score mejora para encontrar el movimiento óptimo.
            Aquí también se debe implementar la poda alpha-beta.
            """
            _, child_score = minimax(game_copy, depth - 1, alpha, beta)
            if child_score > score:
                score = child_score
                best_move = move

            # Actualizar el valor de alpha
            alpha = max(alpha, score)

            # Realizar poda alpha-beta si es posible
            if beta <= alpha:
                break

        return (best_move, score)

    else:

        score = math.inf
        best_move = ("0", "0")
        for move in valid_moves:
            # Se hace una copia del juego para simular jugadas sin afectar el juego actual
            game_copy = copy.deepcopy(game)

            # Se realiza la jugada simulada
            utils.ejecutar_jugada(game_copy, move[0], move[1])

            """
            Aplicar el algoritmo en el caso de que se minimice.
            Se tiene que llamar recursivamente a minimax con la profundidad reducida en 1, 
            y comprobar si el score mejora para encontrar el movimiento óptimo.
            Aquí también se debe implementar la poda alpha-beta.
            """
            _, child_score = minimax(game_copy, depth - 1, alpha, beta)
            if child_score < score:
                score = child_score
                best_move = move

            # Actualizar el valor de beta
            beta = min(beta, score)

            # Realizar poda alpha-beta si es posible
            if beta <= alpha:
                break

        return (best_move, score)
