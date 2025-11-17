from django.test import SimpleTestCase
from django.conf import settings
from unittest.mock import patch, MagicMock
import requests.exceptions

# Importe as funções que você quer testar
from .tmdb import (
    get_headers, 
    search_movie, 
    movie_details, 
    movie_credits, 
    watch_providers, 
    trending_movies,
    now_playing_movies
)

# Constantes para os testes
BASE_URL = "https://api.themoviedb.org/3/"
FAKE_TOKEN = "meu-token-de-teste-falso"

class TMDBApiTest(SimpleTestCase):
    def test_headers_com_token(self):
        """
        Testa se _headers() constrói o cabeçalho corretamente
        quando o token está configurado no settings.
        """

        headers = get_headers(FAKE_TOKEN)
        expected = f"Bearer {FAKE_TOKEN}"
        self.assertEqual(headers["Authorization"],expected)
            

    def test_headers_sem_token(self):
        """
        Testa se _headers() levanta um RuntimeError se o token não
        estiver configurado.
        """

        with self.assertRaises(RuntimeError) as cm:
            get_headers("")
            
        self.assertIn("TMDB_READ_ACCESS_TOKEN não configurado (.env)", str(cm.exception))

    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_search_movie_sucesso(self, mock_headers, mock_get):
        """
        Testa se search_movie chama a URL e os parâmetros corretos.
        """

        fake_data = {"results": [{"id": 1, "title": "Filme Teste"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_response.raise_for_status.return_value = None
        
        mock_get.return_value = mock_response

        response_data = search_movie("query teste", page=2)

        self.assertEqual(response_data, fake_data)
        
        mock_headers.assert_called_once()

        expected_url = f"{BASE_URL}search/movie"
        expected_params = {
            "query": "query teste", 
            "page": 2, 
            "include_adult": "false", 
            "language": "pt-BR"
        }
        mock_get.assert_called_once_with(
            expected_url, 
            headers={"Authorization": "Bearer fake"}, 
            params=expected_params
        )

    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_movie_details_sucesso(self, mock_headers, mock_get):
        """
        Testa se movie_details chama a URL e os parâmetros corretos.
        """
        fake_data = {"id": 550, "title": "Clube da Luta"}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response_data = movie_details(550)

        self.assertEqual(response_data, fake_data)
        
        expected_url = f"{BASE_URL}movie/550"
        expected_params = {"language": "pt-BR"}
        mock_get.assert_called_once_with(
            expected_url, 
            headers={"Authorization": "Bearer fake"}, 
            params=expected_params
        )

    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_watch_providers_sucesso(self, mock_headers, mock_get):
        """
        Testa se watch_providers chama a URL e os parâmetros corretos.
        (Note que esta chamada não envia 'params')
        """
        fake_data = {"id": 550, "results": {"BR": {}}}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response_data = watch_providers(550)

        self.assertEqual(response_data, fake_data)
        
        expected_url = f"{BASE_URL}movie/550/watch/providers"
        mock_get.assert_called_once_with(
            expected_url, 
            headers={"Authorization": "Bearer fake"}
        )
        
    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_api_http_error(self, mock_headers, mock_get):
        """
        Testa se a exceção de 'requests' é propagada
        (quando raise_for_status() falha).
        """

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            search_movie("query")

    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_movie_credits_sucesso(self, mock_headers, mock_get):
        """
        Testa se movie_credits chama a URL e os parâmetros corretos.
        """
        fake_data = {"id": 550, "cast": [{"name" : "Edward Norton","character": "Narrator"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response_data = movie_credits(550)

        self.assertEqual(response_data, fake_data)
        
        expected_url = f"{BASE_URL}movie/550/credits"
        expected_params = {"language": "pt-BR"}
        mock_get.assert_called_once_with(
            expected_url, 
            headers={"Authorization": "Bearer fake"}, 
            params=expected_params
        )

    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_trending_movies_sucesso(self, mock_headers, mock_get):
        """
        Testa se trending_movies chama a URL e os parâmetros corretos.
        """
        fake_data = {"results": [{"id": 550, "title": "Clube da Luta"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response_data = trending_movies()

        self.assertEqual(response_data, fake_data)
        
        expected_url = f"{BASE_URL}trending/movie/day"
        expected_params = {"language": "pt-BR"}
        mock_get.assert_called_once_with(
            expected_url, 
            headers={"Authorization": "Bearer fake"}, 
            params=expected_params
        )

    @patch('filmes.tmdb.requests.get')
    @patch('filmes.tmdb.get_headers', return_value={"Authorization": "Bearer fake"})
    def test_now_playing_movies_sucesso(self, mock_headers, mock_get):
        """
        Testa se now_playing_movies chama a URL e os parâmetros corretos.
        """
        fake_data = {"results": [{"id": 550, "title": "Clube da Luta"}]}
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response_data = now_playing_movies()

        self.assertEqual(response_data, fake_data)
        
        expected_url = f"{BASE_URL}movie/now_playing"
        expected_params = {"language": "pt-BR", "region": "BR", "page": 1}
        mock_get.assert_called_once_with(
            expected_url, 
            headers={"Authorization": "Bearer fake"}, 
            params=expected_params
        )