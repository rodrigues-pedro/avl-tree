class Tree_Node:

    def __init__(self, key):
        # Inicializa um nó com a key passada pelo usuário
        self.key = key

        # Informações utilizadas para linkar a árvore
        self.parent = None
        self.l_child = None
        self.r_child = None

        # Informações utilizadas para plotar a árvore
        self.x = None
        self.y = None

        # Apenas para AVL
        # Fator de Balanceamento para a AVL
        # No caso da ABB, essa informação não é utilizada
        self.bf = None

    def __repr__(self) -> str:
        """
        Transforma o nó em uma string para ser imprimida ou exibida de alguma forma
        Formato:
        Nó = {
            chave: self.key
            fator de balanceamento: self.bf # Apenas para AVL
        }
        """
        string = "Nó = {<br>"
        string += f"    chave: <b>{self.key}</b><br>"
        if self.bf is not None:
            string += f"    fator de balanceamento: <b>{self.bf}</b><br>"
        string += "}"

        return string

    def is_leaf(self):
        """
        Método que retorna se o nó é folha
        Retorna True se ambos self.l_child e self.r_child forém Nulos(None)
        """
        return (self.l_child is None) & (self.r_child is None)

    def is_left(self):
        """
        Método que retorna se o nó é filho da esquerda do pai dele
        Caso nó seja raiz (pai nulo) -> retorna False
        Caso nó seja filho da direita -> retorna False
        Caso nó seja filho da direita -> retorna True
        """
        if self.parent is None:
            return False
        else:
            return self == self.parent.l_child

    def one_child(self):
        """
        Retorna o filho único se o nó só tiver um filho.
        Caso o nó seja folha, ou tenha dois filhos, retornará None.
        """
        tmp = None

        if (self.l_child is None) & (self.r_child is not None):
            # Se não houver filho da esquerda, e houver da direita
            # Retorna o filho da direita
            tmp = self.r_child
        elif (self.r_child is None) & (self.l_child is not None):
            # Se não houver filho da direita, e houver da esquerda
            # Retorna o filho da esquerda
            tmp = self.l_child

        return tmp

    def rec_search(self, node_key):
        """
        Método que faz a pesquisa recursivamente.

        node_key: int -> chave do nó à ser buscado
        """
        # Se a chave buscada for igual a chave do nó
        # Retorna-se o própio nó
        if self.key == node_key:
            return self

        # Se a chave buscada for menor que a chave do nó
        # Retorna-se a pesquisa recursiva no nó da esquerda
        elif self.key < node_key:
            if self.l_child is not None:
                return self.l_child.rec_search()
            # Caso o nó não tenha filho da esquerda, ergue-se uma exceção:
            raise Exception("Chave não encontrada!")

        # Se a chave buscada for maior que a chave do nó
        # Retorna-se a pesquisa recursiva no nó da direita
        else:
            if self.r_child is not None:
                return self.r_child.rec_search()
            # Caso o nó não tenha filho da direita, ergue-se uma exceção:
            raise Exception("Chave não encontrada!")
