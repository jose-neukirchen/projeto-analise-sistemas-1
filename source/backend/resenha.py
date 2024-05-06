class Resenha:
    def __init__(self, movie_id, nota, texto=None):
        self.movie_id = movie_id
        self.texto = texto
        self.nota = nota