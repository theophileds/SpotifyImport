"""
spotipyImport Usage: main.py --input <file> [--name <name>] [--private]

Options:
  -h, --help         Show this screen.
  -i, --input <file> Input file name
  -n, --name <name>  Name of the playlist (optional). Enclose in quotes if it contains spaces. [default: <file>]
  -p --private       Set the playlist as private [default: False]
"""

import json
import logging

import spotipy
from docopt import docopt
from thefuzz import fuzz

from spotipy.oauth2 import SpotifyOAuth

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

class spotipyImport:
    def __init__(self):
        self.sp_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public, playlist-modify-private'))
        self.sp_id = self.sp_client.current_user()['id']

    @classmethod
    def load_playlist_from_json(cls, filename):
        try:
            with open(filename, 'r') as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(e)
            exit(0)

    def search_music_from_playlist(self, playlist):
        if playlist:
            matched_tracks = []
            for artist, tracks in playlist.items():
                for track in tracks:
                    query = self.sp_client.search(q='{} {}'.format(artist, track), type='track')
                    if 'tracks' in query:
                        # Check if there is a matched song with a ratio of 90
                        match = next((spotify_track['id'] for spotify_track in query['tracks']['items'] if fuzz.ratio(spotify_track['name'], track) >= 90), None)
                        if match:
                            logging.info('There is a match for: {} - {}'.format(artist, track))
                            matched_tracks.append(match)
                        else:
                            logging.warning('No match for: {} - {}'.format(artist, track))
                    else:
                        logging.warning('Nothing found for: {} - {}'.format(artist, track))
            return matched_tracks
        else:
            logging.warning('Playlist is empty')
            exit(0)

    def generate_playlist(self, name, tracks, private):
        playlist = self.sp_client.user_playlist_create(self.sp_id, name, public=not private)
        self.sp_client.playlist_add_items(playlist['id'], tracks)
        logging.info('Playlist {} successfully created!'.format(name))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    input= arguments.get('--input')
    name = arguments.get('--name').replace('<file>', input.replace('.json', ''))
    private = arguments.get('--private')
    
    spotipy_import = spotipyImport()
    playlist = spotipy_import.load_playlist_from_json(input)
    tracks = spotipy_import.search_music_from_playlist(playlist)
    spotipy_import.generate_playlist(name, tracks, private) 
