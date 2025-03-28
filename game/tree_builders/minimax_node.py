import sys
sys.path.append('game')
from tree_builders.tree_node import TreeNode

class MiniMaxTreeNode(TreeNode):
    def __init__(self, number, p1_turn: bool = True, scores=[0, 0], bank=0):
        self.divide_by_2 = None
        self.divide_by_3 = None
        
        super().__init__(number, p1_turn, scores, bank)
        
        if self.finished: # aprēķina strupceļa virsotnes heiristisko vērtējumu
            (p1, p2) = self.scores.copy()
            if self.p1_turn:
                p1 += self.bank # pievieno spēlētājam banku
            else:
                p2 += self.bank    
            self.bank = 0
            self.value = 1 if p1 > p2 else 0 if p1 == p2 else -1
        else: self.value = None

    def make_child(self, number, p1_turn, scores, bank):
        return MiniMaxTreeNode(number, p1_turn, scores, bank) # aizvieto make_child vērtību ar MiniMax koku, lai saknes bērni ģenerētos korekti

    
    def algorithm(self):
        if self.value: return self.value # ja vērtība zināma, atgriež to uzreiz

        val = max(
            [i.algorithm() for i in self.children]) if self.p1_turn else min([i.algorithm() for i in self.children]
            # atkarībā no spēlētāja, virsotnes vērtība ir vai nu lielākā, vai mazākā no bērnu virsotnēm
        )
        return val

