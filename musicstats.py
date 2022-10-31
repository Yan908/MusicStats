import matplotlib.pyplot as plt  # Used for making and editing the graphs.
import pandas as pd  # Used for creating a dataframe, which transform the informations generated
# into rows and colums, which makes the process of creating the graphs much easier.
import seaborn as sns  # Used for create a simple bar plot graph, to make the reading much easier.
import spotipy  # The official Spotify API for Python.
import tekore as tk  # Another Spotify API but not official, which was made to be
# possible to extract data from playlists with more than 100 tracks.
from datetime import datetime, timedelta  # Both used for converting the duration of the track registered in milliseconds to actual time
from requests.exceptions import ReadTimeout  # Used for handle the request error, which is unfortunately unavoidable.
from spotipy.oauth2 import SpotifyClientCredentials as Scc  # Used for inserting the credentials of the user,
# which is the client ID and the client secrets(Both acessible by simply logging into
# https://developer.spotify.com/dashboard/ and accessing "My Applications").


class MusicStats:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    # Just a remind that I don't have all the rights for this mini repository,
    # since I mainly used the https://github.com/plamere/spotipy and https://github.com/felix-hilden/tekore.

    def stats(self, playlist_links: [list, str],
              name: str,
              show_image: bool = True,
              save_image: bool = True,
              return_dict: bool = False):
        """An function which will generate an simple bar plot which these following parameters:

Danceability: Measures how much does the song create a dancing desire on the person who are listening to it.
Energy: Measures how energetic the song is.
Speechiness: Show how frequent is the vocalist singing throught the entire song by making
a simple ratio between the time the siinger sang and the duration of the song.
Acousticness: Measures how many acoustic instruments/elements there is in the song.
Instrumentalness: Measures how many instrumental elements are there.*
Valence: Measures how happy/cheerful/positive the song is.
*It's different from acousticness since it also includes synthetic instruments.

The bar plot graph basically shows the arithmetic mean of all parameters of the playlist.
Extra function tools:

save_image: If True, it will save the image on your desktop as "{name} comparison.png"
return_dict: If True, returns the dict with all parameters on the playlist

Attention: Althrought the function was made to accept many playlists, always be aware about the
lenght of the playlists you are inserting because the longer the playlist,
the longer it will take to return the function value(Could even take couple of minutes
and can also generate an unavoidable server request error)."""
        try:
            client_credentials_manager = Scc(client_id=self.client_id, client_secret=self.client_secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            token = tk.request_client_token(client_id=self.client_id, client_secret=self.client_secret)
            spotify = tk.Spotify(token)
            tracks, track_ids = [], []
            if type(playlist_links) == list:
                for it in playlist_links:
                    items = spotify.playlist_items(it.replace("https://open.spotify.com/playlist/", ""))
                    t_next = spotify.all_items(items)
                    for i in range(items.total):
                        item = t_next.__next__()
                        tracks.append(item)
                        track_ids.append(tracks[i].track.id)
            else:
                items = spotify.playlist_items(playlist_links.replace("https://open.spotify.com/playlist/", ""))
                t_next = spotify.all_items(items)
                for i in range(items.total):
                    item = t_next.__next__()
                    tracks.append(item)
                    track_ids.append(tracks[i].track.id)
            danceability = []
            energy = []
            speechiness = []
            acousticness = []
            instrumentalness = []
            valence = []
            for i in range(len(track_ids)):
                part_of_link = track_ids[i]
                link = f"https://open.spotify.com/track/{part_of_link}"
                info = sp.audio_features(link)[0]
                if info is None:
                    pass
                else:
                    danceability.append(info['danceability'])
                    energy.append(info['energy'])
                    speechiness.append(info['speechiness'])
                    acousticness.append(info['acousticness'])
                    instrumentalness.append(info['instrumentalness'])
                    valence.append(info['valence'])

            dance = round(sum(danceability) / len(danceability), 3)
            hooray = round(sum(energy) / len(energy), 3)
            speak = round(sum(speechiness) / len(speechiness), 3)
            acoustic = round(sum(acousticness) / len(acousticness), 3)
            instrument = round(sum(instrumentalness) / len(instrumentalness), 3)
            happy = round(sum(valence) / len(valence), 3)

            informations = [dance, hooray, speak, acoustic, instrument, happy]
            parameters = ['Danceability', 'Energy', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Valence']
            values = pd.DataFrame({"Music Parameters": parameters, "Values": informations})
            plt.figure(figsize=(10, 10), edgecolor="red")
            splot = sns.barplot(x="Music Parameters", y="Values", data=values)
            splot.set_ylim(0, 1)
            plt.xlabel("Music Parameters", size=20)
            plt.ylabel("Values", size=20)
            plt.bar_label(splot.containers[0], size=10, label_type='center')
            plt.suptitle(f"{name.capitalize()} Stats", size=30)
            plt.title(f"Used {len(track_ids)} tracks for comparison")
            if save_image is True:
                plt.savefig(f"{name.lower()} comparison.png")
            if show_image is True:
                plt.show()
            if return_dict is True:
                return dict(zip(parameters, informations))
            else:
                return "Image generated sucessfully."
        except ReadTimeout:
            return "Server error connection. Either it's network request error " \
                   "or you are just asking to handle playlist that are really long."

    def stats_track(self, track_link: str,
                    show_image: bool = True,
                    save_image: bool = True,
                    return_dict: bool = False):
        """Works on the same was as the function stats, except it only accepts one song."""
        try:
            client_credentials_manager = Scc(client_id=self.client_id, client_secret=self.client_secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            link = f"https://open.spotify.com/track/{track_link.replace('https://open.spotify.com/track/', '')}"
            info = sp.audio_features(link)[0]
            if info is None:
                raise TypeError("Couldn't return Spotify music analysis. Reason: NoneType object is not subscriptable.")
            else:
                danceability = round(info["danceability"], 3)
                energy = round(info["energy"], 3)
                speechiness = round(info["speechiness"], 3)
                acousticness = round(info["acousticness"], 3)
                instrumentalness = round(info["instrumentalness"], 3)
                valence = round(info["valence"], 3)

                informations = [danceability, energy, speechiness, acousticness, instrumentalness, valence]
                parameters = ['Danceability', 'Energy', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Valence']
                values = pd.DataFrame({"Music Parameters": parameters, "Values": informations})
                plt.figure(figsize=(10, 10), edgecolor="red")
                splot = sns.barplot(x="Music Parameters", y="Values", data=values)
                splot.set_ylim(0, 1)
                plt.xlabel("Music Parameters", size=20)
                plt.ylabel("Values", size=20)
                plt.bar_label(splot.containers[0], size=10, label_type='center')
                track = sp.track(link)['album']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                plt.suptitle(f"{track_name} Stats", size=30)
                plt.title(f"Stats from the song {track_name} by {artist_name}.")
                if save_image is True:
                    plt.savefig(f"{artist_name.lower()} - {track_name.lower()}_comparison.png")
                if show_image is True:
                    plt.show()
                if return_dict is True:
                    return dict(zip(parameters, informations))
                else:
                    return "Image generated sucessfully."

        except ReadTimeout:
            return "Server error connection. Either it's network request error " \
                   "or you are just asking to handle playlist that are really long."

    def playlist_info(self, playlist_link: str,
                      ignore_none_values: bool = True):
        """A simple function that retrieves all the important data from spotify data API.
Here's the following keys that the function returns:


Name: The playlist name.

Owner: The playlist owner.

Description: The playlist description.

Playlist ID: The playlist ID.

Playlist Link: The playlist link that the user used.

Image: The playlist image in the biggest size avaliable.

Tracks IDs: A list of all the tracks IDs that are in the playlist.

Followers: The number of the playllist followers.

Color: The primary color of the playlist.

Is Public?: A boolean value telling whenever the playlist is public or not.

Is Collaborative?: A boolean value telling whenever the playlist is collaborative or not.


Extra function tools:

ignore_none_values: If True, remove all values that is None."""
        client_credentials_manager = Scc(client_id=self.client_id, client_secret=self.client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        token = tk.request_client_token(client_id=self.client_id, client_secret=self.client_secret)
        spotify = tk.Spotify(token)
        playlist = sp.playlist(playlist_link.replace("https://open.spotify.com/playlist/", ""))
        tracks, track_ids = [], []
        items = spotify.playlist_items(playlist_link.replace("https://open.spotify.com/playlist/", ""))
        t_next = spotify.all_items(items)
        for i in range(items.total):
            item = t_next.__next__()
            tracks.append(item)
            track_ids.append(tracks[i].track.id)
        info = {"Name": playlist['name'],
                "Owner": playlist['owner']['display_name'],
                "Description": playlist['description'],
                "Playlist ID": playlist['id'],
                "Playlist Link": playlist['external_urls']['spotify'],
                "Image": playlist['images'][0]['url'],
                "Track IDs": track_ids,
                "Followers": f"{playlist['followers']['total']} followers",
                "Color": playlist['primary_color'],
                "Is Public?": playlist['public'],
                "Is Collaborative": playlist['collaborative']}
        if ignore_none_values is True:
            new_info = {k: v for k, v in info.items() if v is not None}
            return new_info
        return info

    def track_info(self, track_link: str,
                   ignore_none_values: bool = True):
        """The same as playlist_info(), except it only work for singles and have these parameters:


Artist Name: The artist name.

Artist ID: The artist ID.

Artist Link: The link of the artist.

Song Name: The name of the song.

Song Link: The song link you just used.

Song Cover: The album cover of the song.

Release Date: The day the song was released officially.

Key: The key of the song in american format.

Tempo: The tempo of the song.

Song Lenght: The duration of the song.


Also returns all of the parameters that are also returned on stats_track() function."""
        try:
            client_credentials_manager = Scc(client_id=self.client_id, client_secret=self.client_secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            link = f"https://open.spotify.com/track/{track_link.replace('https://open.spotify.com/track/', '')}"
            info = sp.audio_features(link)[0]
            if info is None:
                raise TypeError("Couldn't return Spotify music analysis. Reason: NoneType object is not subscriptable.")
            else:
                track = sp.track(track_link)['album']
                date = track['release_date']
                day, month, year = date[-2:], date[5:-3], date[:4]
                notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
                mode = ['Major', 'Minor']
                lenght = timedelta(seconds=info['duration_ms'] // 1000)
                actual_lenght = datetime.strptime(str(lenght), "%H:%M:%S").isoformat(timespec='seconds').replace("1900-01-01T", "")
                if actual_lenght.startswith("00:"):
                    result = actual_lenght[3:]
                else:
                    result = actual_lenght
                all_informations = {'Artist Name': track['artists'][0]['name'],
                                    'Artist ID': track['artists'][0]['id'],
                                    'Artist Link': track['artists'][0]['external_urls']['spotify'],
                                    'Song Name': track['name'],
                                    'Song Link': track['external_urls']['spotify'],
                                    'Song Cover': track['images'][-1]['url'],
                                    'Release Date': f'{day}/{month}/{year}',
                                    'Key': f"{notes[info['key']]} {mode[info['mode']]}",
                                    'Tempo': round(info['tempo']),
                                    'Song Lenght': result,
                                    'Danceability': round(info["danceability"], 3),
                                    'Energy': round(info["energy"], 3),
                                    'Speechiness': round(info["speechiness"], 3),
                                    'Acousticness': round(info["acousticness"], 3),
                                    'Instrumentalness': round(info["instrumentalness"], 3),
                                    'Valence': round(info["valence"], 3)}
                if ignore_none_values is True:
                    new_informations = {k: v for k, v in all_informations.items() if v is not None}
                    return new_informations
                return all_informations
        except ReadTimeout:
            return "Server error connection. Either it's network request error " \
                       "or you are just asking to handle playlist that are really long."

    def album_info(self, album_link: str,
                   ignore_none_values: bool = True):
        """Just like track_info, it works the same as playlist_info(), except it only work for albums and have these parameters:


Artist Name: Returns the name of the artist of the album.

Artist ID: The artist ID.

Artist Link: The link of the artist.

Album Name: Returns the name of the album.

Album ID: Returns the album id.

Album Link: Returns the album link that it was used.

Album Cover: Returns the album cover in the biggest size avaliable.

Release Date: Returns the day the album was released.

Number of Tracks: Returns the number of the tracks on the album.

Track IDs: Returns an dict showing its numeration and all the track IDs of the album, respectively.

Label: Returns the label where this album was released.

'Copyright': Returns who holds the right of the album, generally the label where the album was released.

'Genres': Returns a list of the genres of the album.

'Popularity': Returns the album popularity i a scale of 0 to 1."""
        client_credentials_manager = Scc(client_id=self.client_id, client_secret=self.client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        token = tk.request_client_token(client_id=self.client_id, client_secret=self.client_secret)
        spotify = tk.Spotify(token)
        album = sp.album(album_link)
        album_tracks = spotify.album_tracks(album_link.replace("https://open.spotify.com/album/", ""))
        track_id = [item.id for item in album_tracks.items]
        number = [f"Track {i+1}" for i in range(len(track_id))]
        number[0], number[len(number) // 2], number[-1] = "Intro", "Interlude", "Outro"
        date = album['release_date']
        day, month, year = date[-2:], date[5:-3], date[:4]
        informations = {'Artist Name': album['artists'][0]['name'],
                        'Artist ID': track['artists'][0]['id'],
                        'Artist Link': track['artists'][0]['external_urls']['spotify'],
                        'Album Name': album['name'],
                        'Album ID': album['id'],
                        'Album Link': album['external_urls']['spotify'],
                        'Album Cover': album['images'][0]['url'],
                        'Release Date': f"{day}/{month}/{year}",
                        'Number of Tracks': album['total_tracks'],
                        'Track IDs': dict(zip(number, track_id)),
                        'Label': album['label'],
                        'Copyright': f"{album['copyrights'][0]['text']} ©",
                        'Genres': album['genres'],
                        'Popularity': album['popularity'] / 100}
        if ignore_none_values is True:
            new_informations = {k: v for k, v in informations.items() if v != []}
            return new_informations
        return informations
