import sqlite3, json
from datetime import datetime

DB_PATH = 'simulacoes.db'
class Database: 
    def conectar():
        return sqlite3.connect(DB_PATH)
    
    def criar_tabela():
        conn = Database.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                idade INTEGER NOT NULL,
                perfil TEXT NOT NULL,
                resultado TEXT NOT NULL,
                investimento_inicial REAL,
                tempo_meses INTEGER,
                aporte_mensal REAL,
                criado_em TEXT NOT NULL
            )
        ''')
        conn.commit()
    def salvar_simulacao(nome, email, simulacao, perfil, resultado, investimento_inicial, tempo_meses, aporte_mensal):
    # Garante que a tabela exista antes de salvar
        Database.criar_tabela()

        conn = Database.conectar()
        cursor = conn.cursor()

        idade = simulacao.get("idade", 0)
        criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO simulacoes (
                nome, email, idade, perfil, resultado,
                investimento_inicial, tempo_meses, aporte_mensal, criado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nome, email, idade,
            json.dumps(perfil),
            json.dumps(resultado),
            investimento_inicial,
            tempo_meses,
            aporte_mensal,
            criado_em
        ))

        conn.commit()
        conn.close()
        print(">>> Salvando simulação no banco de dados...")
        print("Nome:", nome)
        print("Email:", email)
        print("Investimento inicial:", investimento_inicial)
        
    def buscar_simulacoes_por_email(email):
        conn = Database.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nome, idade, perfil, resultado, investimento_inicial, tempo_meses, aporte_mensal, criado_em
            FROM simulacoes
            WHERE email = ?
            ORDER BY criado_em DESC
        ''', (email,))
        rows = cursor.fetchall()
        conn.close()
        return rows
