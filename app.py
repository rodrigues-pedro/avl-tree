import streamlit as st
from ABB import AVL_Tree


st.set_page_config(
    page_title="Árvore AVL",
    page_icon="🌲",
)

if 'tree' not in st.session_state:
    st.session_state.tree = AVL_Tree()

c30, c32 = st.columns([7, 2])

with c30:
    st.title("🌲 Árvore Binária de Busca")
    st.header("")


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

with cf:
    with st.form(key="my_form"):
        operacao = st.radio(
            "Qual operação você deseja fazer?",
            ["Inserir Nó", "Remover Nó", "Buscar um Nó", "Deletar a Árvore"],
            # help="",
        )

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
