class Filme:
    def __init__(self, id, titulo, descricao, nota_media, poster):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.nota_media = nota_media
        self.poster = poster
        self.resenhas = []

    def adicionar_resenha(self, resenha):
        self.resenhas.append(resenha)

    def calcular_nota_media(self):
        if not self.resenhas:
            return 0
        total = sum(resenha.nota for resenha in self.resenhas)
        return total / len(self.resenhas)