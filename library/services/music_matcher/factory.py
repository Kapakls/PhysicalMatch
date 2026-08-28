from library.services.discogs.factory import create_discogs_service
from library.services.spotify.factory import create_spotify_service

from .service import MusicService


def create_music_service() -> MusicService:
    return MusicService(
        spotify_service=create_spotify_service(),
        discogs_service=create_discogs_service(),
    )
