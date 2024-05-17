
  
# SpotifyImport
  
Hi and Welcome to SpotifyImport,    
    
This script allows you to import playlists from Json files to Spotify. It uses thefuzz library to match songs based on Levenshtein distance.

## How to use it  
First you need to install dependencies with Pipenv

    pipenv install

  Then activate the virtual environment  

     pipenv shell 

You will need to define environment variables that contain your Spotify API credentials

    export SPOTIPY_CLIENT_ID='your-spotify-client-id'
    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
    export SPOTIPY_REDIRECT_URI='http://localhost/callback'

> Have a look on https://developer.spotify.com/ on how to generate your own API keys

You will also need to define a **callback_uri**, i.e: *http://localhost/callback*

Run the script!
  
    python main.py --input kit_sebastian_playlist.json
    python main.py --input kit_sebastian_playlist.json --name "Kit Sebastian Playlist (Pandora)"
    python main.py --input kit_sebastian_playlist.json --name "Kit Sebastian Playlist (Pandora)" --private

## Ok cool, but how to generate a Json file?
[PandoraExport](https://github.com/Doritos250/PandoraExport) can generate playlist files in Json.

> Other tools like PandoraExport are in preparation, stay tuned!

If you want to create your own playlist Json files, you need to follow the following schema:  

    {  
      "Artist1": [  
        "Song1"  
      ],  
      "Artist2": [  
        "Song1"  
      ],  
      "Artist3": [  
        "Song1",
        "Song2",
        "Song3"  
      ]
    }

## More information about the libraries used:

thefuzz: https://github.com/seatgeek/thefuzz

Spotipy: https://github.com/spotipy-dev/spotipy

Docopt: https://github.com/docopt/docopt
