class TreeNode:
    def __init__(self, number, p1_turn: bool = True, scores = [0, 0], bank=0):
        # katram koka elementam pievienojam spēles stāvokļus
        self.number = int(number)
        self.scores = scores.copy()
        self.bank = bank
        self.children = []
        self.p1_turn = p1_turn # kurš spēlētājs izpilda gājienu; p1 = cilvēks
        self.finished = (self.number <= 10) or not (self.number % 2 == 0 or self.number % 3 == 0)
        # uzreiz izveidojam elementam bērnus (un viņi arī sev rekursīvi izveidos bērnus)
        if scores == [0,0]: self.generate_children()
    
    def __eq__(self, node2): # funkcija spēles stāvokļu salīdzināšanai (node1 == node2)
        if node2 is None: return False
        return (
            self.number == node2.number and
            self.scores == node2.scores and
            self.bank == node2.bank and
            self.p1_turn == node2.p1_turn
        )
    
    def __str__(self): # izvada elementu smuki
        return f"n={self.number}, scores={self.scores}, bank={self.bank}, children={len(self.children)}, player1:{self.p1_turn}, finished={self.finished}"
    
    def __hash__(self):
         return hash((self.number, self.scores[0], self.scores[1], self.bank, self.p1_turn))
    
    def make_child(self, number, p1_turn, scores, bank): # šo funkciju būs jāmaina atvasinātās klasēs
        return TreeNode(number, p1_turn, scores, bank)

    def add_child(self, child):
        self.children.append(child)
        if (self.number / 2) == child.number:
            self.divide_by_2 = child
        else:
            self.divide_by_3 = child
    
    def generate_children(self, generated_nodes = {}):
        def add_child(child):
            # funkcija pārbauda, vai elements jau bija ģenerēts. Ja ir - jaunu neizveido, pievieno jau eksistējošo
            if hash(child) in generated_nodes:
                self.add_child( generated_nodes[hash(child)] ) # TODO: node still generates its children
            else:
                self.add_child(child.generate_children(generated_nodes))
                generated_nodes[hash(child)] = child
        
        if self.finished: return self
        
        if self.number % 2 == 0: # ja skaitlis dalās ar 2
            scores = self.scores.copy()
            bank = self.bank

            # pievieno preteniekam 2 punktus (atkarībā no tā, kurš spēlētājs izdarīja gājienu)
            if self.p1_turn:
                scores[1] += 2
            else:
                scores[0] += 2
            if (self.number / 2) % 5 == 0: bank += 1 # pievieno 5 punktus bankai
            add_child( self.make_child(self.number/2, not self.p1_turn, scores, bank) ) # pievieno elementu kokam (no make_child)


        if self.number % 3 == 0: # same here bet ar 3
            scores = self.scores.copy()
            bank = self.bank

            if self.p1_turn:
                scores[0] += 3
            else:
                scores[1] += 3
            if (self.number / 3) % 5 == 0: bank += 1
            add_child( self.make_child(self.number/3, not self.p1_turn, scores, bank) )

        return self
    
    def vertiba(self):
        win = self.scores[0] - self.scores[1] # spēlētāju punktu starpība - lielāka=labāka
        moves = (2 if self.number % 2 == 0 else 0) + (-3 if self.number % 3 == 0 else 0) # cik punktu pretinieks var iegūt nākamajā gājienā
        bank = self.bank # bankas punkti, lielāki=labāki

        return win + moves + bank # kopēja vērtība ir summa no 3 faktoriem
