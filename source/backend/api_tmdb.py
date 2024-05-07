import requests
from source.backend.filme import Filme

class API_TMDb:
    def __init__(self, api_key):
        self.api_key = api_key
        print(api_key)
        self.base_url = "https://api.themoviedb.org/3"

    def definir_diretor(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}/credits?language=pt"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            crew = response.json().get('crew', [])
            diretor = None
            for member in crew:
                if member['job'] == 'Director':
                    diretor = member['name']
                    break
            return diretor
        else:
            return None
        

    def definir_elenco(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}/credits?language=pt"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            cast = response.json().get('cast', [])
            elenco = []
            for member in cast:
                if member['order'] <= 3:
                    elenco.append(member['name'])
            return elenco
        else:
            return None


    def buscar_filmes_trending(self):
        url = f"{self.base_url}/trending/movie/day?language=pt"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            filmes_trending = response.json().get('results', [])
            filmes = []
            for filme_info in filmes_trending:
                filme = Filme(
                    id=filme_info["id"],
                    titulo=filme_info["title"],
                    descricao=filme_info["overview"],
                    nota_media=filme_info["vote_average"],
                    poster=filme_info["poster_path"]
                )
                filmes.append(filme)
            return filmes
        else:
            return None
        
    def buscar_detalhes_filme(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}?language=pt"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            filme_info = response.json()  # Retorna diretamente o objeto do filme
            generos_filme = [genero['name'] for genero in filme_info["genres"]]
            filme = Filme(
                id=filme_info["id"],
                titulo=filme_info["title"],
                descricao=filme_info["overview"],
                nota_media=filme_info["vote_average"],
                poster=filme_info["poster_path"],
                generos=generos_filme,  # Usa a lista de nomes dos gêneros
                data_lancamento=filme_info["release_date"],  # Corrigido: data_lancamento
                lingua=filme_info["original_language"],
                duracao=filme_info["runtime"],
                pais=filme_info["origin_country"],
                diretor=self.definir_diretor(filme_info["id"]),
                elenco_principal=self.definir_elenco(filme_info["id"])
            )
            return filme
        else:
            return None
        
    def buscar_filme(self, movie_title):
        url = f"{self.base_url}/search/movie?query={movie_title}&include_adult=false&language=pt&page=1"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            filmes_search = response.json().get('results', [])
            filmes = []
            for filme_info in filmes_search:
                filme = Filme(
                    id=filme_info["id"],
                    titulo=filme_info["title"],
                    descricao=filme_info["overview"],
                    nota_media=filme_info["vote_average"],
                    poster=filme_info["poster_path"]
                )
                filmes.append(filme)
            return filmes
        else:
            return None
        
    def buscar_filme_por_id(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}?language=pt"
        print(url)
        headers = {"accept": "application/json", "Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code == 200:
            filme_info = response.json()  # Retorna diretamente o objeto do filme
            generos_filme = [genero['name'] for genero in filme_info["genres"]]
            filme = Filme(
                id=filme_info["id"],
                titulo=filme_info["title"],
                descricao=filme_info["overview"],
                nota_media=filme_info["vote_average"],
                poster=filme_info["poster_path"],
                generos=generos_filme,  # Usa a lista de nomes dos gêneros
                data_lancamento=filme_info["release_date"],  # Corrigido: data_lancamento
                lingua=filme_info["original_language"],
                duracao=filme_info["runtime"],
                pais=filme_info["origin_country"]
            )
            return filme
        else:
            return None