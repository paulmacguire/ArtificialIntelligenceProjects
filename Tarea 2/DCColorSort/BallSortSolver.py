import pygame
import time
import json
import os

import BallSortBack
from binary_heap import BinaryHeap
from node import Node
import heuristics

HEURISTIC_PONDERATOR = 1
VISUALIZATION = False
MOVING_SPEED = 15

# Replace with the map to be tested
GAME_MAP = "map_1"

# Compute the map's absolute path
relative_map_path = os.path.join("maps", f"{GAME_MAP}.json")
current_path = os.path.dirname(os.path.realpath(__file__))
MAP_PATH = os.path.join(current_path, relative_map_path)

# Load the map's data
with open(MAP_PATH, 'r') as f:
    MAP_DATA = json.load(f)

class AStarSolver():

    '''
        This class models the solver for the game and performs the A* algorithm in order to find a solution for it.
    '''

    def __init__(self, heuristic=heuristics.wagdy_heuristic, visualization=VISUALIZATION, map_info=MAP_DATA):
        '''
            Parameters:
                heuristic (function) : function used as heuristic for the search (should take a State as an input and output a number), no heuristic by default.
                visualization (bool) : whether to or not to display the solution after it's found.

        '''

        self.expansions = 0
        self.generated = 0

        # Load the map's data
        self.game = BallSortBack.BallSortGame()
        self.game.load_map(map_info)
        self.initial_state = self.game.init_state

        self.heuristic = heuristic
        self.open = BinaryHeap()

        if visualization:
            self.game.start_visualization(text="Solving...")

        self.nodes_in_memory = 0  # Variable para contar los nodos en memoria

    # Varias partes del código, tanto del método search(), cómo lazysearch(), fueron debuggeados con
    # la ayuda de ChatGPT, y también fue basado en el código visto en clases del método search (A*)

    def search(self):
        '''
        Realiza la búsqueda A* para encontrar una solución.
        '''
        self.start_time = time.process_time()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        # initial_node.h = heuristics.wagdy_heuristic(initial_node.state)
        initial_node.key = HEURISTIC_PONDERATOR*initial_node.h
        self.open.insert(initial_node)

        self.generated = {}
        self.generated[self.initial_state] = initial_node

        while not self.open.is_empty():
            n = self.open.extract()
            self.game.current_state = n.state
            if n.state.is_final():
                print("Entrando al if de n.state.is_final()")
                self.end_time = time.process_time()
                return n.trace(), self.expansions, self.end_time - self.start_time
            
            succesors = self.game.get_valid_moves()
            # print(f"Este es el succesors: {succesors}")
            # print(f"Este es el succesors, obtenido por los get_valid_moves(): {succesors}")
            self.expansions += 1
            for child_state, action, cost in succesors:
                # print(f"Este es el child_state: {child_state}")
                child_node = self.generated.get(child_state)
                # print(f"Este es el child_nodes: {child_nodes}")
                is_new = child_node is None
                path_cost = n.g + cost

                if is_new or path_cost < child_node.g:
                    if is_new:
                        child_node = Node(child_state, n)
                        self.generated[child_state] = child_node

                    child_node.action = action
                    child_node.g = path_cost
                    child_node.key = HEURISTIC_PONDERATOR * child_node.h #Acá se implementó el Greedy Best First Search
                    # Si se cambia la linea 101 por: child_node.key = child_node.g + HEURISTIC_PONDERATOR * child_node.h
                    # Se puede ver que el código funciona de manera correcta. Sin embargo, al haber implementado Greedy Best First Search, el código no arroja una solución.
                    self.open.insert(child_node)
            
        self.end_time = time.process_time()
        return None




    def lazysearch(self):
        '''
        Realiza la búsqueda Lazy A* para encontrar una solución.
        '''
        self.start_time = time.process_time()
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.key = HEURISTIC_PONDERATOR * initial_node.h
        self.open.insert(initial_node)
        self.generated = {}
        self.generated[self.initial_state] = initial_node

        while not self.open.is_empty():
            n = self.open.extract()
            self.game.current_state = n.state
            if n.state.is_final():
                self.end_time = time.process_time()
                return n.trace(), self.expansions, self.end_time - self.start_time

            successors = self.game.get_valid_moves()
            self.expansions += 1
            for child_state, action, cost in successors:
                child_node = Node(child_state, n)
                is_new = child_state not in self.generated

                path_cost = n.g + cost
                if is_new or path_cost < child_node.g:
                    child_node.action = action
                    child_node.g = path_cost
                    child_node.key = HEURISTIC_PONDERATOR * child_node.h  #Acá se implementó el Greedy Best First Search
                    # Si se cambia la linea 142 por: child_node.key = child_node.g + HEURISTIC_PONDERATOR * child_node.h
                    # Se puede ver que el código funciona de manera correcta. Sin embargo, al haber implementado Greedy Best First Search, el código no arroja una solución.
                    self.open.insert(child_node)
                    if is_new:
                        self.generated[child_state] = child_node
            
        self.end_time = time.process_time()
        return None



if __name__ == "__main__":
    # We create an instance for the solver and perform the search on the current map
    solver = AStarSolver(
        heuristic=heuristics.wagdy_heuristic, visualization=VISUALIZATION)
    print(f"Creando el sol.....")
    sol = solver.search()

    # In case a solution was found, try it out
    if sol[0] is not None:
        solver.game.current_state = solver.game.init_state
        for step in sol[0][1]:
            solver.game.make_move(step[0], step[1], moving_speed=MOVING_SPEED)

        if VISUALIZATION:
            solver.game.front.draw(solver.game.current_state, text=":)")
            pygame.time.wait(8000)
            pygame.quit()

        print("The search was succesful at finding a solution.")
        print(f"The number of expansions: {solver.expansions}")
        print(
            f"The time it took to find a solution: {solver.end_time - solver.start_time}")
        print(f"Number of steps: {len(sol[0][1])}")
