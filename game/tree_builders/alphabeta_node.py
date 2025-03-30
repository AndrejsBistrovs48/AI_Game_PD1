import sys
sys.path.append('game')
from tree_builders.minimax_node import MiniMaxTreeNode
import time

class AlphaBetaTreeNode(MiniMaxTreeNode):
    def __init__(self, number, p1_turn = True, scores=[0,0], bank=0):
        super().__init__(number, p1_turn, scores, bank) # koks tiek ģenerēts tāds pats kā MiniMax, mainās tikai algoritms

    def make_child(self, number, p1_turn, scores, bank):
        return AlphaBetaTreeNode(number, p1_turn, scores, bank) # aizvieto make_child vērtību ar MiniMax koku, lai saknes bērni ģenerētos korekti

    def algorithm(self, alpha = float('-inf'), beta = float('+inf'), top_call=True):
        start_time = time.time_ns() if top_call else None

        if self.finished: return self.value, 1

        nodes_visited = 1
        best_child = None # glābājam info par labāko gājienu
        value = None

        if self.p1_turn: # ja ir maksimizātora gājiens
            value = float('-inf') # virsotnes vērtība, sākumā mīnus bezgalība
            for ch in self.children:
                child_value, counter = ch.algorithm(alpha, beta, False)
                nodes_visited += counter # pievienojam counteram apmēklētas vērtības no rekursijas
                if child_value > value:
                    value = child_value # maksimums no esošas virsotnes vērtības un tiko aprēķināta bērna
                    best_child = ch
                alpha = max(alpha, value) # mainām alfa
                if alpha >= beta: break # <— šeit nogriešana, tālāk vērtības neaprēķinam
        else:
            value = float('inf')
            for ch in self.children:
                child_value, counter = ch.algorithm(alpha, beta, False)
                nodes_visited += counter
                if child_value < value:
                    value = child_value # minimums no virsotnes vērtības un bērna
                    best_child = ch
                beta = min(beta, value)
                if alpha >= beta: break # <— šeit notiek beta nogriešana

        if top_call:
            return best_child, nodes_visited, time.time_ns() - start_time
        else: return value, nodes_visited