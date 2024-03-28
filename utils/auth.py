# # import spotipy
# # from spotipy.oauth2 import SpotifyClientCredentials
# #
# # # Reemplaza 'tu_client_id' y 'tu_client_secret' con tus propias credenciales
# # client_id = 'tu_client_id'
# # client_secret = 'tu_client_secret'
# #
# # # Crea una instancia de SpotifyClientCredentials con tus credenciales
# # client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# #
# # # Crea una instancia de Spotipy pasando el gestor de credenciales
# # sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# #
# # # Obtiene un token de acceso
# # token_info = client_credentials_manager.get_access_token()
# #
# # # Extrae el token de acceso
# # token = token_info['access_token']
# #
# # print("Token de acceso:", token)
#
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
#
#
# def get_spotify():
#     auth_manager = get_token()
#     sp = spotipy.Spotify(auth_manager=auth_manager)
#
#     return sp
#
#
# def get_token():
#     return SpotifyClientCredentials(client_id="68c011b650b54bac9451529eec23d6f3", client_secret="e645ead70c8b4fa0b16a96dcfe64c30d").get_access_token()
import os

import requests
import dotenv


# Define los parámetros necesarios
import requests
import base64
from dotenv import load_dotenv
load_dotenv()
# Datos de la aplicación
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Codificar las credenciales en base64
credentials = f"{client_id}:{client_secret}"
credentials_b64 = base64.b64encode(credentials.encode()).decode()

# URL de la autenticación de Spotify
auth_url = 'https://accounts.spotify.com/api/token'

# Scopes requeridos
scopes = [
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-public',
    'playlist-modify-private',
    'user-library-read',
    'user-library-modify',
    'user-read-recently-played',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-email',
    'user-read-private'
]

# Parámetros de la petición POST
payload = {
    'grant_type': 'client_credentials',
    'scope': ' '.join(scopes)
}

# Cabeceras de la petición POST
headers = {
    'Authorization': f'Basic {credentials_b64}'
}

# Realizar la petición POST para obtener el token
response = requests.post(auth_url, data=payload, headers=headers)

