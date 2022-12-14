# MusicStats
An simple project that you can see the average status from one or multiple playlists based on spotify API and return an autogenerated image with all status showed for you.

## Conditions

To start using, you need to create a new application by accesing https://developer.spotify.com/dashboard/ and login with your account. </br>
After that, create an new app and get the client id and the client secret of that app.

<h3> Also it needs to use these followings packages: </h3>

- matplotlib
- pandas
- seaborn
- spotipy
- tekore

## Usage

<h3> To start, set up the project: </h3>

```py
from musicstats import MusicStats

CLIENT_ID = "Your client ID"
CLIENT_SECRET = "Your client secret"

ms = MusicStats(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
```

<h3> To get the music stats by playlists: </h3>

```py
print(ms.stats("42EZ7AoyAisnG6k8Sza6SV", name="Dubstep", save_image=True, show_image=True, return_dict=True))
```

Result:

![dubstep comparison](https://user-images.githubusercontent.com/102044040/199076320-b334c463-1174-40c6-9d6b-37e3accde196.png)

```
{'Danceability': 0.524, 'Energy': 0.913, 'Speechiness': 0.193, 'Acousticness': 0.023, 'Instrumentalness': 0.262, 'Valence': 0.234}
```

<h4> Parameters of this function: </h4>

- playlist_links: Playlist Link or ID(Mandatory), can be either a list of playlists or just one playlist
- name: The name you wanna save the stats(Also Mandatory)
- show_file: If True, it shows the archive(Default: True)
- save_file: If True, it saves the archive on your file(Default: True)
- return_dict: If True, it will return the dict with the same data showed on the image but with dict format(Default: False)

<h3> To get the music stats by a specific track: </h3>

```py
print(ms.stats_track("1BocvYKP6Khn2AXOLqNmUS", save_image=True, show_image=True, return_dict=True))
```

Result:

![zomboy - dead man walking pt  1_comparison](https://user-images.githubusercontent.com/102044040/199075318-69b24c68-b909-4176-b0e7-afa23e70c9f5.png)

```
{'Danceability': 0.46, 'Energy': 0.963, 'Speechiness': 0.086, 'Acousticness': 0.004, 'Instrumentalness': 0.1, 'Valence': 0.052}
```

<h2> Extra functions: </h3>

These extra functions are just the adaptations of the spotify JSON database for tracks, albuns and playlists. </br>
These are:

- track_info
- album_info
- playlist_info

<h4> All of them have the same parameters: </h4>

- link: Insert the link or the id of the track/album/playlist you wanna check the info.
- ignore_none_values: If True, it removes all the keys which have None value(Default: True)

Example:

```py
print(ms.track_info("1BocvYKP6Khn2AXOLqNmUS", ignore_none_values=True))
```

Result:

```
{'Artist Name': 'Zomboy', 'Artist ID': '0ycHhPwPvoaO4VGzmMnXGq', 'Artist Link': 'https://open.spotify.com/artist/0ycHhPwPvoaO4VGzmMnXGq', 'Song Name': 'Dead Man Walking Pt. 1', 'Song Link': 'https://open.spotify.com/album/5Rulijsb8lWwqPSFbzEHgD', 'Song Cover': 'https://i.scdn.co/image/ab67616d0000b273815904ad6320c068275243e0', 'Release Date': '22/07/2022', 'Key': 'Ab Minor', 'Tempo': 150, 'Song Lenght': '04:47', 'Danceability': 0.46, 'Energy': 0.963, 'Speechiness': 0.086, 'Acousticness': 0.004, 'Instrumentalness': 0.1, 'Valence': 0.052}
```
