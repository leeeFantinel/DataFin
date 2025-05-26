import streamlit as st

class Options:
    def mostrar_menu(self):
        st.write("### Perfil do Investidor")
        
        risco = st.selectbox(
            "Qual o seu nível de tolerância ao risco? 1 para baixo(conservador), 2 para médio (moderado) e 3 para alto (arrojado)",
            options=["1 - Baixo", "2 - Médio", "3 - Alto"]
        )
        conhecimento = st.selectbox(
            "Nível de conhecimento sobre investimentos",
            options=["1 - Básico", "2 - Intermediário", "3 - Avançado"]
        )
        objetivo = st.selectbox(
            "Qual seu objetivo principal com os investimentos?",
            options=['1 - Aumentar o patrimônio', '2 - Segurança financeira', '3 - Aposentadoria', '4 - Viagem dos sonhos', '5 - Outros']
        )
        
        # Extrair só o número da escolha para manter compatibilidade com análise
        risco_val = risco[0]
        conhecimento_val = conhecimento[0]
        objetivo_val = objetivo[0]

        # Também retornar a string completa para mostrar na interface e para ViewResults
        return {
            "risco": (risco_val, risco),
            "conhecimento": (conhecimento_val, conhecimento),
            "objetivo": (objetivo_val, objetivo)
        }
