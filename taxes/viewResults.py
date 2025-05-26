import matplotlib.pyplot as plt
import streamlit as st

class ViewResults:
    def __init__(self, investimento_inicial, tempo_meses, aporte_mensal, risco, objetivo):
        self.investimento_inicial = investimento_inicial
        self.tempo_meses = int(tempo_meses)
        self.aporte_mensal = aporte_mensal
        self.risco = risco
        self.objetivo = objetivo

    def display_results(self):
        st.write("### Resumo do investimento")
        st.write(f"Investimento inicial: R$ {self.investimento_inicial:,.2f}")
        st.write(f"Tempo: {self.tempo_meses} meses")
        st.write(f"Aporte mensal: R$ {self.aporte_mensal:,.2f}")
        st.write(f"Perfil de risco: {self.risco}")
        st.write(f"Objetivo: {self.objetivo}")

    def grafico(self):
        meses = list(range(self.tempo_meses + 1))

        historicos = {}
        taxas = {
            'CDB': 0.08,
            'Tesouro Direto (Prefixado)': 0.07,
            'LCI': 0.06,
            'LCA': 0.06,
            'Bitcoin': 0.15,
            'ETF Ações': 0.10,
            'ETF Renda Fixa': 0.05
        }

        for investimento, taxa in taxas.items():
            valores = [self.investimento_inicial]
            for mes in range(1, self.tempo_meses + 1):
                valor = valores[-1] * (1 + taxa / 12) + self.aporte_mensal
                valores.append(valor)
            historicos[investimento] = valores

        plt.figure(figsize=(10, 6))
        for investimento, valores in historicos.items():
            plt.bar(meses, valores, alpha=0.5, label=investimento)

        plt.xlabel("Meses")
        plt.ylabel("Valor do Investimento (R$)")
        plt.title("Evolução dos Investimentos ao Longo do Tempo")
        plt.legend(loc="upper left")
        plt.grid(True)

        st.pyplot(plt)
        plt.clf()  # limpar figura para próximas execuções
