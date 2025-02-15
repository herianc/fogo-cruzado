import streamlit as st
import time

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)


with st.sidebar:
    st.write('Feito por: Herian Cavalcante')
    st.markdown('[GitHub](https://github.com/herianc)')

st.title('Bem-vindo(a)! 👋')

st.header('Instituto Fogo Cruzado')

text1 = '''O Instituto Fogo Cruzado desenvolveu uma metodologia própria e inovadora para monitorar tiroteios nos centros urbanos e seus impactos. 
Produzimos mais de 20 indicadores inéditos sobre violência armada nas regiões metropolitanas do Rio e do Recife e, em breve, em mais cidades brasileiras. 
Através de um aplicativo de celular, o Fogo Cruzado recebe e disponibiliza informações sobre tiroteios e disparos de arma de fogo. 

Acesse para mais informações: [Fogo Cruzado](https://fogocruzado.org.br/).
'''
st.markdown(text1)

st.header('📊 Sobre o Dashboard')

text2 = """Este dashboard reune dados disponibilizados durante o processo seletivo para a vaga de Assessor de Dados Jr. O conjunto de dados contém registros 
de tiroteios e vítimas durante o ano de 2024 nos estados do Rio de Janeiro, Pernambuco e Bahia. 
"""
st.markdown(text2)

st.header('⚙️ Ferramentas utilizadas')
st.markdown("""Este dashboard foi feito utilizando apenas Python, onde as principais bibliotecas foram: 
- Streamlit (UI) 
- Pandas (manipulação de dados)

Utilizei essa stack por já ter familiaridade, mas estou aberto a aprender qualquer ferramenta de BI 🫡.
""")


