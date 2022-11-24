from .Tree_Node import Tree_Node

import plotly.graph_objects as go


class ABB_Tree:
    """
    Árvore de Busca Binária
    """
    def __init__(self):
        # Inicializa uma árvore com a raiz vazia
        self.root = None

    def is_empty(self):
        """
        Método que diz se a árvore está vazia ou não
        Raiz nula -> True
        Raiz não nula -> False
        """
        return self.root is None

    def incert_node(self, node_key):
        """
        Método utilizado para inserir um nó em uma árvore binária de busca
        Mantém a ordenação, porém não faz balanceamento, ou seja, pode desbalancear a árvore
        """
        # inicializa um novo nó com a chave recebida por parâmetro
        new_node = Tree_Node(node_key)

        if self.is_empty():
            # se a árvore for vazia:
            # coloca o novo nó como raiz da árvore
            self.root = new_node
        else:
            # se a árvore não for vazia:
            tmp = self.root
            while True:
                # iremos percorrer a árvore, partindo da raiz
                # caso a chave seja menor que a chave do nó atual:
                if node_key < tmp.key:
                    # se não houver filho para a esquerda
                    if tmp.l_child is None:
                        # adiciona-se o novo nó à esquerda do nó atual
                        new_node.parent = tmp
                        tmp.l_child = new_node
                        break
                    # se houver, passaremos a olhar para o filho da esquerda
                    tmp = tmp.l_child
                # caso a chave seja maior que a chave do nó atual:
                else:
                    # se não houver filho para a direita
                    if tmp.r_child is None:
                        # adiciona-se o novo nó à direita do nó atual
                        new_node.parent = tmp
                        tmp.r_child = new_node
                        break
                    # se houver, passaremos a olhar para o filho da esquerda
                    tmp = tmp.r_child

    def delete_node(self, node_key):
        """
        Método utilizado para remover um nó, recebendo como parâmetro a chave do nó a ser removido
        Mantém a ordenação porém não faz o rebalanceamento.
        """
        # busca o nó a ser removido, utilizando o método de pesquisa
        try:
            to_delete = self.search(node_key)
        except Exception as E:
            raise E

        # busca o nó pai do nó a ser deletado
        parent = to_delete.parent
        # guardamos se o nó a ser deletado é filho da esquerda ou não
        lc = to_delete.is_left()

        # Caso 1: Nó folha
        # { p -> d } passa a ser { p -> None }
        if to_delete.is_leaf():
            # Nó pai do nó a ser deletado para de apontar para esse nó
            if lc:
                parent.l_child = None
            else:
                parent.r_child = None

        else:
            # busca o filho único caso seja único
            oc = to_delete.one_child()

            # Caso 2: Nó com uma subárvore
            # { p -> d -> oc } passa a ser { p -> oc }
            if oc is not None:
                # Nó pai do nó a ser deletado passa a apontar para o filho único do nó a ser deletado
                oc.parent = parent
                if lc:
                    parent.l_child = oc
                else:
                    parent.r_child = oc

            # Caso 3: Nó com duas subárvores
            # { p -> d -> [f_e, f_d] } passa a ser { p -> f_d -> f_e }
            else:
                # Aponta o pai do nó a ser deletado para o filho da direita do nó a ser deletado
                tmp = to_delete.r_child
                tmp.parent = parent
                if lc:
                    parent.l_child = tmp
                else:
                    parent.r_child = tmp

                # busca um nó vazio à esquerda do filho da direita do nó a ser deletado
                while tmp.l_child is not None:
                    tmp = tmp.l_child

                # Aponta o filho da esquerda do nó à ser deletado como
                # filho da esquerda do nó encontrado no loop acima
                tmp.l_child = to_delete.l_child
                to_delete.l_child.parent = tmp

    def search(self, node_key):
        """
        Método para a busca iterativa
        """
        # partimos da raiz da árvore
        tmp = self.root
        while tmp is not None:
            # Se a chave buscada for igual a chave do nó
            # Retorna-se o própio nó
            if tmp.key == node_key:
                return tmp

            # Se a chave do nó for maior que chave buscada
            # Iremos olhar para o nó da esquerda
            elif tmp.key > node_key:
                tmp = tmp.l_child

            # Se a chave do nó for menor que chave buscada
            # Iremos olhar para o nó da direita
            else:
                tmp = tmp.r_child

        # Se chegarmos em uma folha sem encontrar a chave
        # Iremos erguer uma excessão
        raise Exception("Chave não encontrada!")

    def rec_search(self, node_key):
        """
        Busca recursiva
        Chama a busca recursiva no nó raiz da árvore
        """
        return self.root.rec_search(node_key)

    def calculate_depth(self, node="Root"):
        """
        Método que calcula a profundidade de uma árvore recursivamente.

        :Params:
        node:
            str:       Root (default) parte da raiz
            Tree_Node: Partiremos a partir do nó que foi passado como parâmetro
            None:      Consideraremos uma árvore vazia, profundidade zero
        """
        # recebendo a string "Root" como parâmetro, buscaremos a raiz como ponto de partida
        if node == "Root":
            node = self.root

        if node is None:
            # se o nó for nulo, retorna-se zero
            return 0
        elif node.is_leaf():
            # se o nó for folha, retorna-se 1
            # Critério de parada da recursão
            return 1
        else:
            # caso o nó não seja folha, nem nulo
            # Calcula a profundidade das subárvores à esquerda e à direita
            l_depth = self.calculate_depth(node.l_child)
            r_depth = self.calculate_depth(node.r_child)

            # retorna a profundidade máxima + 1
            return max(r_depth, l_depth) + 1

    ######################################## MÉTODOS PARA O PLOT DA ÁRVORE #############################################
    def full_pos(self):
        """
        Cria um dicionário com as possições onde devem ser inseridos nós de acordo com a profundidade da árvore
        Esse dicionário segue o padrão:
        { profundidade: [x para cada nó] para cada profundidade }
        para uma árvore de profundidade 2, será criado o dicionário:
        {
            0 : [1.5]
            1 : [0.5, 2.5]
            2 : [0, 1, 2, 3]
        }
        Isso foi feito para que a árvore seja igualmente distribuída e simétrica
        """
        m_y = self.calculate_depth()
        pos = {}
        n = []

        for i in range(m_y, -1, -1):
            if i == m_y:
                pos[i] = [x for x in range(2 ** i)]
                n.extend([i for _ in range(len(pos[i]))])
            else:
                base = pos[i + 1]
                pos[i] = [(base[j] + base[j + 1]) / 2 for j in range(0, len(base), 2)]
                n.extend([i for _ in range(len(pos[i]))])

        n.reverse()
        return pos, n

    def plot_tree(self):
        """
        Esse método efetivamente cria o plot da árvore
        Basicamente ele percorre a árvore width first, preenchendo as posições retornadas pelo método full_pos
        Ele faz isso preenchendo as listas de coordenadas à serem plotadas, incluíndo apenas as desejadas, cortando os
        vazios.
        E fazendo, de acordo, uma lista com os labels e tooltips, e mais duas para as coordenadas das arestas

        Tendo essas listas prontas, apenas chamamos as funções da biblioteca plotly para gerar o plot
        """
        ## Variaveis Gráfico
        Xn = []
        Yn = []
        Xe = []
        Ye = []
        label = []
        text = []

        pos, n = self.full_pos()

        fila = []
        tmp = self.root

        while tmp is not None:
            label.append(str(tmp.key))
            text.append(str(tmp))

            if tmp.parent is None:
                y = 0
            else:
                y = tmp.parent.y + 1

            tmp.y = y

            Yn.append(-y)
            av_pos = pos[y]

            if tmp.parent is None:
                x = av_pos[0]
            else:
                x_p = tmp.parent.x
                if tmp.is_left():
                    av_pos = list(filter(
                        lambda x: x < x_p,
                        av_pos
                    ))
                    x = av_pos[-1]
                else:
                    av_pos = list(filter(
                        lambda x: x > x_p,
                        av_pos
                    ))
                    x = av_pos[0]

                Ye.extend([-(y - 1), -y, None])
                Xe.extend([x_p, x, None])

            tmp.x = x
            Xn.append(x)

            if tmp.l_child is not None:
                fila.append(tmp.l_child)
            if tmp.r_child is not None:
                fila.append(tmp.r_child)

            if len(fila) == 0: break
            tmp = fila.pop(0)

        ## Inicializa a Figura
        fig = go.Figure()
        ## Inclui Arestas
        fig.add_trace(go.Scatter(
            x=Xe,
            y=Ye,
            name='Arestas',
            mode='lines',
            line=dict(color='rgb(210,210,210)', width=1),
            hoverinfo='none'
        ))
        ## Inclui Nós
        fig.add_trace(go.Scatter(
            x=Xn,
            y=Yn,
            mode='markers',
            name='Node',
            marker=dict(
                symbol='circle-dot',
                size=40,
                color='rgb(255, 75, 75)',  # '#DB4551',
                line=dict(color='rgb(250,250,250)', width=1)
            ),
            text=text,
            hoverinfo='text',
            opacity=0.8
        ))

        ## Cria as anotações
        annotations = []
        font_size = 25
        font_color = 'rgb(250,250,250)'
        for k in range(len(label)):
            annotations.append(
                dict(

                    text=label[k],  # or replace labels with a different list for the text within the circle
                    x=Xn[k], y=Yn[k],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False
                )
            )

        axis = dict(
            showline=False,  # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
        )

        fig.update_layout(
            annotations=annotations,
            font_size=25,
            showlegend=False,
            xaxis=axis,
            yaxis=axis,
            margin=dict(l=40, r=40, b=85, t=100),
            hovermode='closest',
            plot_bgcolor='rgb(14, 17, 23)',
            hoverlabel=dict(
                font=dict(color=font_color, size=16),
            )
        )

        return fig
