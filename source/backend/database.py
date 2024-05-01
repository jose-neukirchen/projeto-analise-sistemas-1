import sqlite3
import json

# Função para criar o banco de dados e as tabelas
def criar_banco_dados():
    # Conecta ao banco de dados (se não existir, será criado)
    conn = sqlite3.connect('usuarios.db')

    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Cria a tabela 'usuarios' se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            watchlist TEXT,
            resenhas TEXT
        )
    ''')

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()

# Função para adicionar um novo usuário ao banco de dados
def adicionar_usuario(nome, senha, watchlist=[], resenhas={}):
    # Conecta ao banco de dados
    conn = sqlite3.connect('usuarios.db')

    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Insere o novo usuário na tabela
    cursor.execute('''
        INSERT INTO usuarios (nome, senha, watchlist, resenhas)
        VALUES (?, ?, ?, ?)
    ''', (nome, senha, json.dumps(watchlist), json.dumps(resenhas)))

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()

# Chama a função para criar o banco de dados e as tabelas
criar_banco_dados()

# # Exemplo de como adicionar um novo usuário ao banco de dados
# adicionar_usuario('usuario1', 'senha1', ['filme1', 'filme2'], {'filme1': 'ótimo', 'filme2': 'bom'})