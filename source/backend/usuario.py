import sqlite3
import json

class Usuario:
    def __init__(self, nome, senha, watchlist=None, resenhas=None):
        self.nome = nome
        self.senha = senha
        self.watchlist = watchlist
        self.resenhas = resenhas

    def get_nome(self):
        return self.nome
    
    def adicionar_resenha(self, movie_id, resenha, nota):
        movie_id = str(movie_id)
        if movie_id not in self.resenhas:
            self.resenhas[movie_id] = []
        self.resenhas[movie_id] = [resenha, nota]  
        self._atualizar_resenhas_no_banco_de_dados()

    def adicionar_filme_watchlist(self, filme):
        self.watchlist.append(filme)
        self._atualizar_watchlist_no_banco_de_dados()

    def _atualizar_resenhas_no_banco_de_dados(self):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET resenhas = ? WHERE nome = ?
        ''', (json.dumps(self.resenhas), self.nome))
        conn.commit()
        conn.close()

    def _atualizar_watchlist_no_banco_de_dados(self):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET watchlist = ? WHERE nome = ?
        ''', (json.dumps(self.watchlist), self.nome))
        conn.commit()
        conn.close()

    @staticmethod
    def criar_banco_dados():
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                watchlist TEXT,
                resenhas TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def adicionar_usuario(nome, senha):
        print(f"Inserindo usuário: {nome}")
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, senha, watchlist, resenhas)
            VALUES (?, ?, ?, ?)
        ''', (nome, senha, json.dumps([]), json.dumps({})))
        conn.commit()
        conn.close()
        print(f"Usuário {nome} inserido com sucesso.")

    @staticmethod
    def validar_login(nome, senha):
        conn = sqlite3.connect('usuarios.db')
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
        
    @staticmethod
    def obter_usuario_pelo_nome(nome):
        conn = sqlite3.connect('usuarios.db')
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
        

    # Método para obter a resenha e a nota do usuário para um filme específico
    def obter_resenha_e_nota(self, movie_id):
        movie_id = str(movie_id)
        if self.resenhas and movie_id in self.resenhas:
            print("ok")
            resenha, nota = self.resenhas[movie_id]
            print(resenha, nota)
            return resenha, nota
        else:
            return None, None