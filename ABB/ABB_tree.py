import plotly.graph_objects as go


class ABB_Tree_Node:
    
    def __init__(self, key):
        self.key = key
        self.parent = None 
        self.l_child = None
        self.r_child = None
        self.x = None
        self.y = None

        ## Apenas para AVL
        self.bf = None

    def __repr__(self) -> str:
        string = "Nó = {<br>"
        string += f"    chave: <b>{self.key}</b><br>"
        if self.bf is not None:
            string += f"    fator de balanceamento: <b>{self.bf}</b><br>"
        string += "}"

        return string

    def is_leaf(self):
        return (self.l_child is None) & (self.r_child is None)

    def is_left(self):
        if self.parent is None:
            return False
        else:
            return self == self.parent.l_child

    def one_child(self):
        tmp = None

        if (self.l_child is None) & (self.r_child is not None):
            tmp = self.r_child
        elif (self.r_child is None) & (self.l_child is not None):
            tmp = self.l_child
        
        return tmp

    def rec_search(self, node_key):
        if self.key == node_key:
            return self
        elif self.key < node_key:
            if self.l_child is not None:
                return self.l_child.rec_search()
            raise Exception("Chave não encontrada!")
        else:
            if self.r_child is not None:
                return self.r_child.rec_search()
            raise Exception("Chave não encontrada!")


class ABB_Tree:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def incert_node(self, node_key):
        new_node = ABB_Tree_Node(node_key)

        if self.is_empty():
            self.root = new_node
        else:
            tmp = self.root
            while (True):
                if node_key < tmp.key:
                    if tmp.l_child is None:
                        new_node.parent = tmp
                        tmp.l_child = new_node
                        break
                    tmp = tmp.l_child
                else:
                    if tmp.r_child is None:
                        new_node.parent = tmp
                        tmp.r_child = new_node
                        break
                    tmp = tmp.r_child

    def delete_node(self, node_key):
        try:
            to_delete = self.search(node_key)
        except Exception as E:
            raise E

        parent = to_delete.parent

        lc = False
        if parent.l_child is not None:
            lc = to_delete.key == parent.l_child.key

        if to_delete.is_leaf():
            if lc:
                parent.l_child = None
            else:
                parent.r_child = None

        else:
            oc = to_delete.one_child()
            if oc is not None:
                oc.parent = parent
                if lc:
                    parent.l_child = oc
                else:
                    parent.r_child = oc
            
            else:
                tmp = to_delete.r_child
                tmp.parent = parent

                if lc:
                    parent.l_child = tmp
                else:
                    parent.r_child = tmp
                
                while tmp.l_child is not None:
                    tmp = tmp.l_child
                
                tmp.l_child = to_delete.l_child
                to_delete.l_child.parent = tmp

    def search(self, node_key):
        tmp = self.root
        while tmp is not None:
            if tmp.key == node_key:
                return tmp
            elif tmp.key > node_key:
                tmp = tmp.l_child
            else:
                tmp = tmp.r_child
        
        raise Exception("Chave não encontrada!")  
    

    def rec_search(self, node_key):
        return self.root.rec_search(node_key)

    def calculate_depth(self, node="Root"):
        if node == "Root":
            node = self.root

        if node is None:
            return 0
        elif node.is_leaf():
            return 1
        else:
            # Calcula a profundidade das sub-árvores
            l_depth = self.calculate_depth(node.l_child)
            r_depth = self.calculate_depth(node.r_child)
    
            # retorna a profundidade máxima + 1
            return max(r_depth, l_depth) + 1

    def full_pos(self):
        m_y = self.calculate_depth()
        pos = {}
        n = []

        for i in range(m_y, -1, -1):
            if i == m_y:
                pos[i] = [x for x in range(2**i)]
                n.extend([i for _ in range(len(pos[i]))])
            else:
                base = pos[i+1]
                pos[i] = [(base[j]+base[j+1])/2 for j in range(0, len(base), 2)]
                n.extend([i for _ in range(len(pos[i]))])

        n.reverse()
        return pos, n

    def plot_tree(self):
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
                
                Ye.extend([-(y-1), -y, None])       
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
                color='rgb(255, 75, 75)',    #'#DB4551',
                line=dict(color='rgb(250,250,250)', width=1)                                
            ),
            text=text,
            hoverinfo='text',
            opacity=0.8
        ))

        ## Cria as anotações
        annotations = []
        font_size=25
        font_color='rgb(250,250,250)'
        for k in range(len(label)):
            annotations.append(
                dict(
                    
                    text=label[k], # or replace labels with a different list for the text within the circle
                    x=Xn[k], y=Yn[k],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False
                )
            )

        axis = dict(
            showline=False, # hide axis line, grid, ticklabels and  title
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



            


        

        





    