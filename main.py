"""spotipyImport

Usage:
  main.py [--input input.json] [--playlist Playlist_Name] [--public True]
  main.py [-h | --help]

Options:
  -h --help                     Show this screen.
  --input=filename              Import file name [default: input.json]
  --playlist=Playlist_Name      Name of the artist with _ instead of space [default: Playlist_Name]

"""

import json
import logging

import spotipy
from docopt import docopt
from thefuzz import fuzz

from spotipy.oauth2 import SpotifyOAuth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class spotipyImport:
    def __init__(self):
        self.sp_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public, playlist-modify-private'))
        self.sp_id = self.sp_client.current_user()['id']

    @classmethod
    def load_playlist_from_json(cls, filename):
        try:
            with open(filename, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError as e:
            logger.error(e)
            exit(0)

    def search_music_from_playlist(self, playlist):
        matched_tracks = []
        for artist, songs in playlist.items():
            artist_name = artist
            for song in songs:
                track_name = song
                query_result = self.sp_client.search(q='{} {}'.format(artist_name, track_name), type='track')
                if 'tracks' in query_result:
                    match = next((spotify_track['id'] for spotify_track in query_result['tracks']['items'] if fuzz.ratio(spotify_track['name'], track_name) >= 90), None)
                    if match:
                        logger.info('There is a match for: {} - {}'.format(artist_name, track_name))
                        matched_tracks.append(match)
                    else:
                        logger.warning('No match for: {} - {}'.format(artist_name, track_name))
                else:
                    logger.warning('Nothing found for: {} - {}'.format(artist_name, track_name))
        return matched_tracks

    def generate_playlist(self, name, tracks, is_public=True):
        playlist = self.sp_client.user_playlist_create(self.sp_id, name, public=is_public)
        self.sp_client.playlist_add_items(playlist['id'], tracks)
        logger.info('Playlist {} successfully created!'.format(name))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    input_filename = arguments.get('--input')
    playlist_name = ' '.join(arguments.get('--playlist').split('_'))

    spotipy_import = spotipyImport()
    import_playlist = spotipy_import.load_playlist_from_json(input_filename)
    matched_songs = spotipy_import.search_music_from_playlist(import_playlist)
    if matched_songs:
        spotipy_import.generate_playlist(playlist_name, matched_songs)
