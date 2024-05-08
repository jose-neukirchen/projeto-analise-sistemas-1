import sqlite3
import json


class Usuario:
    def __init__(self, nome, senha, email, idade, genero, nacionalidade, watchlist=[], resenhas={}, favoritos=[], assistidos=[], bio=None):
        self.nome = nome
        self.senha = senha
        self.email= email
        self.idade = idade
        self.genero = genero
        self.nacionalidade = nacionalidade
        self.watchlist = watchlist
        self.resenhas = resenhas
        self.favoritos = favoritos
        self.assistidos = assistidos
        self.bio = bio


    def get_nome(self):
        return self.nome
    
    def get_watchlist(self):
        return self.watchlist
    
    def get_favoritos(self):
        return self.favoritos
    
    def adicionar_resenha(self, db, resenha):
        movie_id = str(resenha.movie_id)
        if movie_id not in self.resenhas:
            self.resenhas[movie_id] = []
        self.resenhas[movie_id] = [resenha.texto, resenha.nota]  
        db.atualizar_resenhas_no_banco_de_dados(self, resenha)

    def adicionar_bio(self, db, bio):
        self.bio = bio  
        db.atualizar_bio_no_banco_de_dados(self)

    def adicionar_filme_watchlist(self, db, filme_id):
        filme_id = str(filme_id)
        if filme_id in self.watchlist:
            return
        else:
            self.watchlist.append(filme_id)
            db.atualizar_watchlist_no_banco_de_dados(self)

    def adicionar_filme_favoritos(self, db, filme_id):
        filme_id = str(filme_id)
        if filme_id in self.favoritos:
            return
        else:
            self.favoritos.append(filme_id)
            db.atualizar_favoritos_no_banco_de_dados(self)
        

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