"""SpotifyImport

Usage:
  main.py [--input input.json] [--playlist Playlist_Name] [--public True]
  main.py [-h | --help]

Options:
  -h --help                     Show this screen.
  --input=filename              Import file name [default: input.json]
  --playlist=Playlist_Name      Name of the artist with _ instead of space [default: Playlist_Name]

"""

import asyncio
import json
import logging
import webbrowser

import spotify
from docopt import docopt
from fuzzywuzzy import fuzz as matcher

from spotify_setting import spotify_api_config, spotify_credentials

logger = logging.getLogger(__name__)


class SpotifyImport:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    @classmethod
    def load_playlist_from_json(cls, filename):
        try:
            with open(filename, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError as e:
            logger.error(e)
            exit(0)

    async def search_music_from_playlist(self, playlist):
        async with spotify.Client(self.client_id, self.client_secret) as client:
            matched_tracks = []
            for artist, songs in playlist.items():
                artist_name = artist
                for song in songs:
                    track_name = song
                    query_result = await client.search(q='{} {}'.format(artist_name, track_name), types=['track'])
                    if query_result.tracks:
                        match = next((x for x in query_result.tracks if matcher.WRatio(x.name, track_name) >= 90), None)
                        if match:
                            logger.info('There is a match for: {} - {}'.format(artist_name, track_name))
                            matched_tracks.append(match)
                        else:
                            logger.warning('No match for: {} - {}'.format(artist_name, track_name))
                    else:
                        logger.warning('Nothing found for: {} - {}'.format(artist_name, track_name))
            return matched_tracks

    async def generate_playlist(self, authorization_code, name, tracks):
        async with spotify.Client(self.client_id, self.client_secret) as client:
            user = await spotify.User.from_code(client, authorization_code, redirect_uri='http://localhost/callback')
            playlist = await user.create_playlist(name, public=True)
            await playlist.extend(tracks)
            logger.info('Playlist {} successfully created!'.format(name))
            await user.http.close()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    input_filename = arguments.get('--input')
    playlist_name = ' '.join(arguments.get('--playlist').split('_'))

    spotify_auth_endpoint = spotify_api_config['AUTH_URL'] + \
                            '?client_id=' + spotify_credentials['CLIENT_ID'] + \
                            '&redirect_uri=' + spotify_api_config['REDIRECT_URI'] + \
                            '&scope=' + ','.join(spotify.get_required_scopes(spotify.Playlist.add_tracks)) + \
                            '&response_type=code'

    spotify_import = SpotifyImport(spotify_credentials['CLIENT_ID'], spotify_credentials['CLIENT_SECRET'])
    import_playlist = spotify_import.load_playlist_from_json(input_filename)
    loop = asyncio.get_event_loop()
    matched_songs = loop.run_until_complete(spotify_import.search_music_from_playlist(import_playlist))
    if matched_songs:
        webbrowser.open(spotify_auth_endpoint)
        oauth_code = input('Please copy and paste the token after code parameter from the url: ')
        loop.run_until_complete(spotify_import.generate_playlist(oauth_code, playlist_name, matched_songs))
