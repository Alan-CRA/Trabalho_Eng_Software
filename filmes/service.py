import requests
from django.conf import settings

class TmdbApiService:
    def __init__(self):
        """
        Inicializa o serviço, configurando a sessão do requests.
        """
        self.base_url = settings.TMDB_API_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        self.read_token = settings.TMDB_READ_ACCESS_TOKEN
    
    def get_genres(self):
        url = self.base_url + "genre/movie/list?language=pt"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.read_token
        }

        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_movies_by_name(self,name):
        url = self.base_url + f"search/movie?query={name}&include_adult=false&language=pt-BR&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.read_token
        }

        response = requests.get(url, headers=headers)

        return response.json()
    
    def get_movies_credit(self,movie_id):
        url = self.base_url + f"movie/{movie_id}/credits?language=pt-br"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.read_token
        }

        response = requests.get(url, headers=headers)

        return response.json()
    
    def get_movies_providers(self,movie_id):
        url =  self.base_url + f"movie/{movie_id}/watch/providers"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.read_token
        }

        response = requests.get(url, headers=headers)

        return response.json()