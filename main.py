import streamlit as st, re, os, json, base64, datetime
from taxes import Options, AnalisePerfil, ViewResults, Database

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def idade_valida(idade):
    if idade < 18:
        st.warning("Você deve ter pelo menos 18 anos para usar este simulador.")
        return False
    return True

def buscar_simulacoes_por_email(email_login):
    st.subheader("📚 Histórico de Simulações")
    simulacoes = Database.buscar_simulacoes_por_email(email_login)
    if not simulacoes:
        st.info("Nenhuma simulação encontrada para este e-mail.")
        return

    filtro_nome = st.text_input("🔍 Filtrar por nome (opcional):")

    for sim in simulacoes:
        nome, idade, perfil_json, resultado_json, investimento_inicial, tempo_meses, aporte_mensal, criado_em = sim
        perfil = json.loads(perfil_json)
        resultado = json.loads(resultado_json)

        if filtro_nome and filtro_nome.lower() not in nome.lower():
            continue

        with st.expander(f"{nome} - {criado_em}"):
            st.write(f"**Idade:** {idade}")
            st.write(f"**E-mail:** {email_login}")
            st.write(f"**Perfil:** {perfil.get('risco')} / {perfil.get('objetivo')}")
            st.write(f"**Investimento Inicial:** R$ {investimento_inicial:,.2f}")
            st.write(f"**Aporte Mensal:** R$ {aporte_mensal:,.2f}")
            st.write(f"**Tempo:** {tempo_meses} meses")
            st.write(f"**Sugestão:** {resultado.get('investimento_sugerido')}")
            st.write("**Retornos estimados:**")
            for inv, val in resultado.get('retornos_estimulados', {}).items():
                st.write(f"- {inv}: R$ {val:,.2f}")

def main():
    st.markdown("""
        <style>
            .main {
                background-color: #FBF6F1;
                color: #003366;
            }
            h1, h2, h3 {
                color: #0052cc;
            }
            .stRadio > div {
                flex-direction: row;
            }
            .stButton button {
                background-color: #0052cc;
                color: white;
                border-radius: 8px;
                padding: 0.5em 1em;
                border: none;
            }
            .stButton button:hover {
                background-color: #ffffff;
            }
            .logo-container {
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 1000;
        }

        .logo-container img {
            width: 140px; /* ajuste o tamanho da logo */
        }

        header {visibility: hidden;}
        .block-container {
            padding-top: 100px;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color:#0052cc;'>💰 Simulador de Investimentos <span style='color:#052C9C;'>DataFin</span></h1>", unsafe_allow_html=True)
    # Codifica a imagem em base64 para embutir diretamente no HTML
    with open("logoDataFin.png", "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode()
    st.markdown("""
    <div class="logo-container">
        <img src="data:image/png;base64,{}" alt="Logo DataFin">
    </div>
    """.format(logo_base64), unsafe_allow_html=True)
    
    st.markdown("""
        <p style='text-align: center; color:#052C9C; font-size: 1.2em;'>
            Descubra o melhor investimento para o seu perfil e objetivos financeiros!
        </p>
    """, unsafe_allow_html=True)
    

    st.markdown("## 🔐 Login")
    email_login = st.text_input("Digite seu e-mail para acessar ou salvar simulações:")

    if not validar_email(email_login):
        st.warning("Digite um e-mail válido para continuar.")
        st.stop()

    st.success(f"🔓 Login realizado como: {email_login}")

    menu = st.radio("Navegar:", ["Simulação", "Histórico"])

    if menu == "Simulação":
        nome = st.text_input("Digite seu nome completo:")
        idade = st.number_input("Digite sua idade:", step=1, min_value=0)

        if not idade_valida(idade):
            st.stop()

        investimento_inicial = st.number_input("Valor para investir (R$):", min_value=0.0, step=100.0)
        tempo_meses = st.text_input("Tempo do investimento (em meses)", placeholder="Ex: 12, 24, 36...")
        if not tempo_meses.isdigit() or int(tempo_meses) <= 0:
            st.warning("Digite um número válido de meses para o investimento.")
            st.stop()
        aporte_mensal = st.number_input("Aporte mensal (R$):", min_value=0.0, step=50.0)

        opcoes = Options()
        perfil = opcoes.mostrar_menu()

        if st.button("Calcular"):
            taxas_anuais = {
                'LCI': 0.08,
                'Tesouro Direto (Prefixado)': 0.10,
                'ETF (Ibovespa)': 0.12,
                'CDB': 0.13,
                'Bitcoin': 0.25
            }

            analise = AnalisePerfil(investimento_inicial, tempo_meses, aporte_mensal)
            resultado = analise.analisar(
                risco=perfil['risco'][0],
                conhecimento=perfil['conhecimento'][0],
                objetivo=perfil['objetivo'][0],
                taxas_anuais=taxas_anuais
            )

            st.subheader(f"Sugestão de investimento para {nome}:")
            st.write(resultado["investimento_sugerido"])

            st.subheader("Retornos estimados:")
            for investimento, valor in resultado["retornos_estimulados"].items():
                st.write(f"- {investimento}: R$ {valor:,.2f}")

            explicacoes = {
                'LCI': 'Investimento de baixo risco, isento de Imposto de Renda para pessoa física.',
                'Tesouro Direto (Prefixado)': 'Título público com rentabilidade definida, ideal para objetivos de médio prazo.',
                'ETF (Ibovespa)': 'Fundo que replica o índice da bolsa, com maior risco, indicado para diversificação e longo prazo.',
                'CDB': 'Produto bancário de renda fixa, com bom retorno e risco moderado, sujeito ao FGC.',
                'Bitcoin': 'Criptomoeda volátil, com alto risco e potencial de alto retorno. Ideal para perfis arrojados.'
            }

            sugestao = resultado["investimento_sugerido"]
            st.markdown(f"### 💡 Explicação sobre {sugestao}:")
            st.write(explicacoes.get(sugestao, "Informação não disponível."))

            st.markdown("#### 📌 Boas práticas:")
            st.write("- Sempre diversifique seus investimentos.")
            st.write("- Reavalie seus objetivos periodicamente.")
            st.write("- Nunca invista mais do que está disposto a perder (principalmente em ativos de risco).")

            st.markdown("#### 📈 Gráfico de evolução do investimento:")
            view = ViewResults(investimento_inicial, tempo_meses, aporte_mensal,
                               perfil['risco'][1], perfil['objetivo'][1])
            view.display_results()
            view.grafico()

            # Salvar dados
            simulacao = {
                'nome': nome,
                'email': email_login,
                'idade': idade,
                'perfil': perfil,
                'resultado': resultado,
                'tempo_meses': tempo_meses,
                'aporte_mensal': aporte_mensal,
                'investimento_inicial': investimento_inicial
            }
            Database.salvar_simulacao(
                nome, email_login, simulacao, perfil, resultado,
                investimento_inicial, tempo_meses, aporte_mensal
            )
            st.success("Simulação salva com sucesso!")


    elif menu == "Histórico":
        Database.buscar_simulacoes_por_email(email_login)
        st.write(buscar_simulacoes_por_email(email_login))
        

if __name__ == "__main__":
    main()
