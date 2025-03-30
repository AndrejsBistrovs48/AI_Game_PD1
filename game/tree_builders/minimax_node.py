import sys
sys.path.append('game')
from tree_builders.tree_node import TreeNode
import time

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

    
    def algorithm(self, top_call = True):
        start_time = time.time() if top_call else None
        
        if self.finished: return self.value, 1 # ja vērtība zināma (beigu punkts), atgriež to uzreiz

        # vienā rindiņā iegūstam katram bērnam sarakstu (bērns, bērna vērtība 1/0/-1, cik virsotnes ir zem bērna)
        children = [(child, *child.algorithm(False)) for child in self.children]
        node_count = sum(counter for _,_, counter in children) + 1 # summējam visas virsotnes lai iegūtu kopējo apmēklēto virsotņu skaitu

        best_node, best_value = max(children, key=lambda x: x[1])[:2] if self.p1_turn else min(children, key=lambda x: x[1])[:2] # iegūstam best choice, bērnu vērtības (saraksta 2. elements)


        if top_call: 
            return best_node, node_count, time.time() - start_time
        else: return best_value, node_count