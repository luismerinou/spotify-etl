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
