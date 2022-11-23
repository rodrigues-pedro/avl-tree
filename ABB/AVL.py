from ABB import ABB_Tree

class AVL_Tree(ABB_Tree):
    def __init__(self):
        return super(AVL_Tree, self).__init__()

    def get_balancing_factor(self, node):        
        h_r = self.calculate_depth(node.r_child)
        h_l = self.calculate_depth(node.l_child)

        return h_r - h_l 

    def update_balancing_factor(self):
        fila = []
        tmp = self.root

        while tmp is not None:
            tmp.bf = self.get_balancing_factor(tmp)

            if tmp.l_child is not None:
                fila.append(tmp.l_child)
            if tmp.r_child is not None:
                fila.append(tmp.r_child)

            if len(fila) == 0: break
            tmp = fila.pop(0)


    def left_rotate(self, node):
        if isinstance(node, int):
            node = self.search(node)
        
        node_r = node.r_child

        node.r_child = node_r.l_child
        if node_r.l_child is not None:    
            node_r.l_child.parent = node
        
        node_r.parent = node.parent
        if node.parent is None:
            self.root = node_r
        elif node == node.parent.l_child:
            node.parent.l_child = node_r
        else:
            node.parent.r_child = node_r

        node_r.l_child = node
        node.parent = node_r     

    def right_rotate(self, node):
        if isinstance(node, int):
            node = self.search(node)

        node_l = node.l_child

        node.l_child = node_l.r_child
        if node_l.r_child is not None:    
            node_l.r_child.parent = node
        
        node_l.parent = node.parent
        if node.parent is None:
            self.root = node_l
        elif node == node.parent.l_child:
            node.parent.l_child = node_l
        else:
            node.parent.r_child = node_l

        node_l.r_child = node
        node.parent = node_l
    
    def rebalance(self, node, bf):
        if bf > 0:
            # Sub-árvore da direita maior
            bf_child = self.get_balancing_factor(node.r_child)
            if bf_child > 0:
                # Caso 1: Subárvore direita do filho à direita
                self.left_rotate(node)
            else:
                # Caso 2: Subárvore esquerda do filho à direita
                self.right_rotate(node.r_child)
                self.left_rotate(node)
        else:
            # Sub-árvore da esquerda maior
            bf_child = self.get_balancing_factor(node.l_child)
            if bf_child > 0:
                # Caso 3: Subárvore direita do filho à esquerda
                # Simétrico Caso 2
                self.left_rotate(node.l_child)
                self.right_rotate(node)
            else:
                # Caso 4: Subárvore esquerda do filho à esquerda
                # simétrico Caso 1
                self.right_rotate(node)

    def incert_node(self, node_key):
        super(AVL_Tree, self).incert_node(node_key)

        node = self.search(node_key)
        while node is not None:
            bf = self.get_balancing_factor(node)
           
            if bf > 1 or bf < -1:
                self.rebalance(node, bf)
            
            node = node.parent

        self.update_balancing_factor()

    def delete_node(self, node_key):
        node = self.search(node_key)
        node = node.parent

        super(AVL_Tree, self).delete_node(node_key)

        while node is not None:
            bf = self.get_balancing_factor(node)
           
            if bf > 1 or bf < -1:
                self.rebalance(node, bf)
            
            node = node.parent
            
        self.update_balancing_factor()
