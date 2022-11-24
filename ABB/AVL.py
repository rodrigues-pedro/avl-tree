from ABB import ABB_Tree


class AVL_Tree(ABB_Tree):
    """
    Classe que vai herdar a Árvore de Busca Binária e adicionar as caracteristicas específicas da Árvore AVL
    """

    def __init__(self):
        """
        Inicializa a árvore normalmente, com a raiz nula
        Chamando o método da classe pai
        """
        super(AVL_Tree, self).__init__()

    def get_balancing_factor(self, node):
        """
        Método que calcula o fator de balanceamento
        Calcula-se a profundidade da árvore à esquerda e à direita
        Subtrai-se a direita menos a da esquerda
        """
        h_r = self.calculate_depth(node.r_child)
        h_l = self.calculate_depth(node.l_child)

        return h_r - h_l

    def update_balancing_factor(self):
        """
        Método que percorre toda a árvore depth-first
        atualizando os fatores de balanceamento de cada nó

        Esse método é utilizado após o rebalanceamento para atualizar os fatores de balanceamento
        """
        fila = []
        tmp = self.root

        # Loop para percorrer a árvore depth first
        while tmp is not None:
            # atualiza o fator de balanceamento de cada nó, ao percorrer a árvore
            tmp.bf = self.get_balancing_factor(tmp)

            if tmp.l_child is not None:
                fila.append(tmp.l_child)
            if tmp.r_child is not None:
                fila.append(tmp.r_child)

            if len(fila) == 0: break
            tmp = fila.pop(0)

    def left_rotate(self, node):
        """
        Método que implementa a rotação à esquerda em torno do nó passado como parâmetro
        Esse parâmetro pode receber tanto um int, nesse caso buscaremos o nó usando a pesquisa iterativa
        ou o objeto Tree_Node em si, dessa forma pularíamos esse primeiro passo
        """
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
        """
        Método que implementa a rotação à direita em torno do nó passado como parâmetro
        Esse parâmetro pode receber tanto um int, nesse caso buscaremos o nó usando a pesquisa iterativa
        ou o objeto Tree_Node em si, dessa forma pularíamos esse primeiro passo

        Simétrico ao método left_rotate
        """
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
        """
        Faz o rebalanceamento da árvore
        recebendo um nó e seu fator de rebalanceamento como parâmetros

        Ele implementa os algoritmos descritos como rebalanceamento após a incerção
        Pois, tendo uma árvore desbalanceada, sabendo que iremos atualizar todos os fatores de balanceamento,
        Esse procedimento é o suficiente para rebalancear qualquer árvore,
        desde que o caminho ascendente inteiro seja percorrido
        """
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

    def busca_desbalanceamento(self, node):
        """
        Método que percorre o caminho ascendente partindo de um nó
        E efetua os rebalanceamentos nescessários
        """
        # Percorremos o caminho ascendente, partindo do nó recebido como parâmetro
        # buscando uma necessidade de rebalanceamento
        while node is not None:
            bf = self.get_balancing_factor(node)

            if bf > 1 or bf < -1:
                # Caso encontra-se um nó com |fator de balanceamento| > +-1
                # é feito o rebalanceamento em torno desse nó
                self.rebalance(node, bf)

            node = node.parent

        # Atualizamos todos o fatores de balanceamento
        self.update_balancing_factor()

    def incert_node(self, node_key):
        """
        Método que insere um novo nó
        Primeiro inserimos o nó como em uma ABB
        Depois fazemos o rebalanceamento caso haja tal necessidade
        """
        # Inserimos o nó como em uma ABB
        super(AVL_Tree, self).incert_node(node_key)

        # Busca o desbalanceamento a partir do nó adicionado
        node = self.search(node_key)
        self.busca_desbalanceamento(node)

    def delete_node(self, node_key):
        """
        Método que deleta um nó
        Primeiro deletamos o nó como em uma ABB
        Depois fazemos o rebalanceamento caso haja tal necessidade
        """
        # Buscamos o nó pai do nó que vai ser deletado
        node = self.search(node_key)
        node = node.parent

        # deletamos o nó como em uma ABB
        super(AVL_Tree, self).delete_node(node_key)

        # Busca o desbalanceamento a partir do nó pai do nó que foi deletado
        self.busca_desbalanceamento(node)
