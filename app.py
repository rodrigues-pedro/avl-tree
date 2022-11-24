## Arquivo que contém as configurações da aplicação
import streamlit as st
from ABB import AVL_Tree

## Configura o título e favicon da pagina web
st.set_page_config(
    page_title="Árvore AVL",
    page_icon="🌲",
)

## Caso não exista uma árvore inicializada, inicializamos uma na sessão do aplicativo
if 'tree' not in st.session_state:
    st.session_state.tree = AVL_Tree()

c30, c32 = st.columns([7, 2])

# Título da aplicação
with c30:
    st.title("🌲 Árvore AVL 🌲")
    st.header("")

# informações sobre os desenvolvedores
with c32:
    with st.expander("ℹ️ - About this app", expanded=False):

        st.write(
            """     
    - Desenvolvedores: 
        - Arthur Monteiro
        - Mateus Kalleb
        - Pedro Manuel Rodrigues
    - Algoritmo e Estrutura de Dados 2
    - Instituição: UFG
    - Discente:  
        - Wanderley Alencar
            """
        )

        st.markdown("")

cf, cp = st.columns([2,7])
## formulário que busca as informações necessárias para testar as funcionalidades
with cf:
    with st.form(key="my_form"):
        # Usuário escolhe a operação
        operacao = st.radio(
            "Qual operação você deseja fazer?",
            ["Inserir Nó", "Remover Nó", "Buscar um Nó", "Deletar a Árvore"],
            # help="",
        )

        # Usuário aponta a chave do nó onde ele pretende fazer a operação
        key = st.number_input(
            "Chave do Nó",
            min_value=-100,
            max_value= 100,
            value=0
           # help="",
        )

        submit_button = st.form_submit_button(label="Atualizar Árvore")

if not submit_button:
    st.stop()

# Operação escolhida é feita no nó de acordo com o que o usuário solicitou
with cp:
    try:
        if operacao == "Inserir Nó":
            st.session_state.tree.incert_node(key)
            
        elif operacao == "Remover Nó":
            st.session_state.tree.delete_node(key)

        elif operacao ==  "Buscar um Nó":
            node = st.session_state.tree.search(key)
            st.write(node)
            
        elif operacao ==  "Deletar a Árvore":
            del st.session_state.tree
            st.session_state.tree = AVL_Tree()
    
        st.plotly_chart(st.session_state.tree.plot_tree())
    except Exception as E:
        st.write(E)
