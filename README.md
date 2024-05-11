
  
# SpotifyImport
  
Hi and Welcome to SpotifyImport,    
    
This script allows you to import songs contained in a Json file into Spotify. It uses the FuzzyWuzzy library to compare strings and finds matches between songs in the input file and songs in Spotify based on the Levenshtein distance.

    More information about how to generate a Json file bellow

    
## How to use it  
First you need to install dependencies with Pipenv  

    pipenv install

  Then activate the virtual environment  

     pipenv shell 

You need to define environement variables containing your Spotify API credentials

    export SPOTIPY_CLIENT_ID='your-spotify-client-id'
    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
    export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

> Have a look on https://developer.spotify.com/ to generate your own API keys

You will also need to define a **callback_uri**, by default the script will use *http://localhost/callback*
If you wan to use a custom one you should specify it:

    export SPOTIFY_REDIRECT_URI=<custom_callback_uri>

Run the script!
  
> For argument parsing reasons you need to replace **space** with **_** instead  
  
    python main.py --input import.json --playlist My_Playlist  

## Ok cool, but how to generate a Json file?
[PandoraExport](https://github.com/Doritos250/PandoraExport) can generate playlist based files in Json format.

> Other tools like PandoraExport are in preparation, stay tuned!

If you want to generate a playlist based Json file your own way you have to respect the following schema:  

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

## More information about libraries:    
thefuzz: https://github.com/seatgeek/thefuzz

Spotipy: https://github.com/spotipy-dev/spotipy

Docopt: https://github.com/docopt/docopt

