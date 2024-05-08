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
                email TEXT NOT NULL,
                idade INTEGER NOT NULL,
                genero TEXT NOT NULL,
                nacionalidade TEXT NOT NULL,
                watchlist TEXT,
                resenhas TEXT,
                favoritos TEXT,
                assistidos TEXT,
                bio TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resenhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id TEXT NOT NULL,
                lista_resenhas TEXT NOT NULL
            )
        ''')

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS filmes (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         movie_id TEXT NOT NULL,
        #         titulo TEXT NOT NULL,
        #         descricao TEXT NOT NULL,
        #         nota_media TEXT NOT NULL,
        #         poster TEXT NOT NULL,
        #         generos TEXT NOT NULL,
        #         resenhas TEXT NOT NULL,
        #         data_lancamento TEXT NOT NULL,
        #         lingua TEXT NOT NULL,
        #         duracao TEXT NOT NULL,
        #         pais TEXT NOT NULL,
        #         diretor TEXT NOT NULL,
        #         elenco_principal TEXT NOT NULL
        #     )
        # ''')


        # Salva as alterações
        conn.commit()

        # Fecha a conexão
        conn.close()

    def adicionar_usuario(self, usuario):
        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Insere o novo usuário na tabela
        cursor.execute('''
            INSERT INTO usuarios (nome, senha, email, idade, genero, nacionalidade, watchlist, resenhas, favoritos, assistidos, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario.nome, usuario.senha, usuario.email, usuario.idade, usuario.genero, usuario.nacionalidade, json.dumps(usuario.watchlist), json.dumps(usuario.resenhas), json.dumps(usuario.favoritos), json.dumps(usuario.assistidos), usuario.bio))

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
            id, nome, senha, email, idade, genero, nacionalidade, watchlist_json, resenhas_json, favoritos_json, assistidos_json, bio  = usuario
            watchlist = json.loads(watchlist_json)
            resenhas = json.loads(resenhas_json)
            favoritos = json.loads(favoritos_json)
            assistidos = json.loads(assistidos_json)
            return Usuario(nome, senha, email, idade, genero, nacionalidade, watchlist, resenhas, favoritos, assistidos, bio)
        else:
            return None

    def atualizar_resenhas_no_banco_de_dados(self, usuario, resenha):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Atualizar a tabela 'usuarios'
        cursor.execute('''
            UPDATE usuarios SET resenhas = ? WHERE nome = ?
        ''', (json.dumps(usuario.resenhas), usuario.nome))

        # Verificar se já existe uma entrada para este filme na tabela 'resenhas' para este usuário
        cursor.execute('''
            SELECT * FROM resenhas WHERE movie_id = ?
        ''', (resenha.movie_id,))

        existing_entry = cursor.fetchone()

        if existing_entry:
            # Se já existe uma entrada, atualizar a lista de resenhas
            existing_resenhas = json.loads(existing_entry[2])
            existing_resenhas[usuario.nome] = [resenha.texto, resenha.nota]

            cursor.execute('''
                UPDATE resenhas SET lista_resenhas = ? WHERE id = ?
            ''', (json.dumps(existing_resenhas), existing_entry[0]))
        else:
            # Se não existe uma entrada, inserir uma nova linha na tabela 'resenhas'
            cursor.execute('''
                INSERT INTO resenhas (movie_id, lista_resenhas) VALUES (?, ?)
            ''', (resenha.movie_id, json.dumps({usuario.nome: [resenha.texto, resenha.nota]})))

        conn.commit()
        conn.close()

    def obter_resenhas_por_id_do_filme(self, movie_id):
        conn = sqlite3.connect(Database.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT lista_resenhas FROM resenhas WHERE movie_id = ?', (movie_id,))
        resenha = cursor.fetchone()
        resenhas = json.loads(resenha[0]) if resenha is not None else {}
        conn.close()
        return resenhas


    def atualizar_watchlist_no_banco_de_dados(self, usuario):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET watchlist = ? WHERE nome = ?
        ''', (json.dumps(usuario.watchlist), usuario.nome))
        conn.commit()
        conn.close()

    def atualizar_favoritos_no_banco_de_dados(self, usuario):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET favoritos = ? WHERE nome = ?
        ''', (json.dumps(usuario.favoritos), usuario.nome))
        conn.commit()
        conn.close()

    def atualizar_bio_no_banco_de_dados(self, usuario):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET bio = ? WHERE nome = ?
        ''', (json.dumps(usuario.bio), usuario.nome))
        conn.commit()
        conn.close()