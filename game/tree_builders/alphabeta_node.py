import sys
sys.path.append('game')
from tree_builders import MiniMaxTreeNode

class AlphaBetaTreeNode(MiniMaxTreeNode):
    def __init__(self, number, p1_turn = True, scores=[0,0], bank=0):
        super().__init__(number, p1_turn, scores, bank) # koks tiek ģenerēts tāds pats kā MiniMax, mainās tikai algoritms

    def make_child(self, number, p1_turn, scores, bank):
        return AlphaBetaTreeNode(number, p1_turn, scores, bank) # aizvieto make_child vērtību ar MiniMax koku, lai saknes bērni ģenerētos korekti

    def algorithm(self, alpha = float('-inf'), beta = float('+inf')):
        if self.value: return self.value

        if self.p1_turn: # ja ir maksimizātora gājiens
            value = float('-inf') # virsotnes vērtība, sākumā mīnus bezgalība
            for ch in self.children:
                value = max(value, ch.algorithm(alpha, beta)) # maksimums no esošas virsotnes vērtības un tiko aprēķināta bērna
                alpha = max(alpha, value) # mainām alfa
                if alpha >= beta: break # <— šeit nogriešana, tālāk vērtības neaprēķinam
        else:
            value = float('inf')
            for ch in self.children:
                value = min(value, ch.algorithm(alpha, beta)) # minimums no virsotnes vērtības un bērna
                beta = min(beta, value)
                if alpha >= beta: break # <— šeit notiek beta nogriešana

        self.value = value # piešķir pašai virsotnei heiristisko vērtējumu
        return value