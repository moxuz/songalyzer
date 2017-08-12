from exceptions import SerializationError


class Song(object):
    title = ""
    album = ""
    artist = ""
    popularity = 0
    duration = ""

    def __init__(self, title, album, artist, popularity, duration):
        self.artist = artist
        self.title = title
        self.album = album
        self.popularity = popularity
        self.duration = duration

    @staticmethod
    def from_spotify(song_dict):
        try:
            artists = [artist['name'] for artist in song_dict['artists']]
            artist = ", ".join(artists)

            title = song_dict['name']
            album = song_dict['album']
            popularity = song_dict['popularity']

            duration_ms = song_dict['duration_ms']
            duration = (duration_ms / (1000 * 60)) % 60
            return Song(
                artist=artist,
                title=title,
                album=album,
                popularity=popularity,
                duration=duration,
            )
        except KeyError as e:
            raise SerializationError("Failed to serialize field \"{}\"".format(e.args[0]))


class Playlist(object):
    songs = []
    owner = ""
    name = ""
    description = ""

    def __init__(self, songs, owner, name, description):
        self.songs = songs
        self.owner = owner
        self.name = name
        self.description = description

    @staticmethod
    def from_spotify(playlist_dict):
        try:
            songs = [Song.from_spotify(song_dict['track']) for song_dict in playlist_dict['tracks']['items']]
            owner = playlist_dict['owner']
            name = playlist_dict['name']
            description = playlist_dict['description']
            return Playlist(
                songs=songs,
                owner=owner,
                name=name,
                description=description,
            )
        except KeyError as e:
            raise SerializationError("Failed to serialize field \"{}\"".format(e.args[0]))
