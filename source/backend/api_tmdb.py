import requests
from source.backend.filme import Filme

class API_TMDb:
    def __init__(self, api_key):
        self.api_key = api_key
        print(api_key)
        self.base_url = "https://api.themoviedb.org/3"

    def buscar_filmes_trending(self):
        url = f"{self.base_url}/trending/movie/day?language=en-US"
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