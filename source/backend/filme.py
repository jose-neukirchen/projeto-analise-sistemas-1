class Filme:
    def __init__(self, id, titulo, descricao, nota_media, poster, generos=None, data_lancamento=None, lingua=None, duracao=None, pais=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.nota_media = nota_media
        self.poster = poster
        self.generos = generos # genres
        self.resenhas = []
        self.data_lancamento = data_lancamento # release_date
        self.lingua = lingua # original_language
        self.duracao = duracao # runtime
        self.pais = pais # origin_country