# Spotify Constants
# API V1 -- https://developer.spotify.com/documentation/general/guides/scopes/
spot_scope = 'user-read-playback-state' # read the player state
spot_version = 'v1' # API end point version
spot_base_url = 'https://api.spotify.com' # API URL
spot_player_endpoint = 'me/player' # endpoint for player requests

spot_player_url = '/'.join((spot_base_url, spot_version, spot_player_endpoint))


# Librespot Constants
libre_base_url = 'http://localhost'
libre_port = 24879
libre_token_endpoint = 'token' # local endpoint for requesting spotify token

libre_token_url = '/'.join((libre_base_url+':'+str(libre_port), 
                            libre_token_endpoint, spot_scope))

# spotify JSON mapping using dictor dotted formatting:
spot_map = {
  'title': 'item.name',
  'artist': 'item.album.artists.0.name',
  'album': 'item.album.name',
  'artwork_url': 'item.album.images.0.url',
  'duration': 'item.duration_ms',
  'player': 'device.name',
  'id': 'item.id',
}
