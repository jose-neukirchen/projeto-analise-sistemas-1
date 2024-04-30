class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.watchlist = []
        self.resenhas = []

    def adicionar_resenha(self, resenha):
        self.resenhas.append(resenha)

    def adicionar_filme_watchlist(self, filme):
        self.watchlist.append(filme)