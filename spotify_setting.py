import os

spotify_credentials = {
    'CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID', '1234567890'),
    'CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET', '0987654321')
}

spotify_api_config = {
    'AUTH_URL': os.getenv('SPOTIFY_AUTH_URL', 'https://accounts.spotify.com/authorize'),
    'REDIRECT_URI': os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost/callback'),
}