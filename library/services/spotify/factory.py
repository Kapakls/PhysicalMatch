import httpx

from .client import SpotifyClient
from .service import SpotifyService


def create_spotify_service() -> SpotifyService:
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0),
    )

    client = SpotifyClient(http_client)

    return SpotifyService(client)