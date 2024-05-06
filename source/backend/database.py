import sqlite3
from source.backend.usuario import Usuario
import json

class Database:
    db_name = 'usuarios.db'

    def __init__(self):
        pass

    def criar_banco_dados(self):
        # Conecta ao banco de dados (se não existir, será criado)
        conn = sqlite3.connect(self.db_name)
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

    def adicionar_usuario(self, nome, senha, watchlist=None, resenhas=None):
        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_name)
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

    @staticmethod
    def validar_login(nome, senha):  # Remove 'self' do argumento
        conn = sqlite3.connect(Database.db_name)  # Acessa o nome do banco de dados diretamente
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM usuarios WHERE nome = ? AND senha = ?
        ''', (nome, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return True
        else:
            return False
        
    @classmethod
    def obter_usuario_pelo_nome(cls, nome):
        conn = sqlite3.connect(Database.db_name)  # Correção aqui: Acessar db_name através de uma instância da classe
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            # Se o usuário foi encontrado, retornar um objeto Usuario com os dados recuperados do banco de dados
            id, nome, senha, watchlist_json, resenhas_json = usuario
            watchlist = json.loads(watchlist_json)
            resenhas = json.loads(resenhas_json)
            return Usuario(nome, senha, watchlist, resenhas)
        else:
            return None


    def atualizar_resenhas_no_banco_de_dados(self, usuario):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET resenhas = ? WHERE nome = ?
        ''', (json.dumps(usuario.resenhas), usuario.nome))
        conn.commit()
        conn.close()

    def atualizar_watchlist_no_banco_de_dados(self, usuario):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET watchlist = ? WHERE nome = ?
        ''', (json.dumps(usuario.watchlist), usuario.nome))
        conn.commit()
        conn.close()
