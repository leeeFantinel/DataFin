class AnalisePerfil:
    def __init__(self, investimento_inicial, tempo_meses, aporte_mensal):
        self.investimento_inicial = investimento_inicial
        self.tempo_meses = int(tempo_meses)
        self.aporte_mensal = aporte_mensal

    def analisar(self, risco, conhecimento, objetivo, taxas_anuais):
        # Sugere investimento principal com base no risco e conhecimento
        if risco == '1':  # Baixo
            investimento_sugerido = 'LCI'
        elif risco == '2':  # Médio
            investimento_sugerido = 'Tesouro Direto (Prefixado)' if conhecimento == '1' else 'ETF (Ibovespa)'
        elif risco == '3':  # Alto
            investimento_sugerido = 'CDB' if conhecimento == '1' else 'Bitcoin'
        else:
            investimento_sugerido = 'LCI'  # fallback
        
        retornos_estimulados = {}
        for investimento, taxa in taxas_anuais.items():
            # Cálculo composto mensal aproximado (simplificado)
            valor = self.investimento_inicial
            for mes in range(self.tempo_meses):
                valor = valor * (1 + taxa / 12) + self.aporte_mensal
            retornos_estimulados[investimento] = valor

        return {
            "investimento_sugerido": investimento_sugerido,
            "retornos_estimulados": retornos_estimulados
        }
