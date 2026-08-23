import urllib.parse

from django.conf import settings

from library.services.spotify.exceptions import (
    SpotifyConfigurationError,
)

from .client import SpotifyClient
from .schemas.album import SpotifyAlbum
from .schemas.common import SpotifyToken
from .schemas.user import SpotifyUser


class SpotifyService:
    def __init__(self, client: SpotifyClient):
        self.client = client

    def get_authorization_url(self) -> str:

        if not settings.SPOTIFY_CLIENT_ID:
            raise SpotifyConfigurationError(
                "Spotify client ID is not configured."
            )

        if not settings.SPOTIFY_REDIRECT_URI:
            raise SpotifyConfigurationError(
                "Spotify redirect URI is not configured."
            )

        params = {
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "scope": settings.SPOTIFY_SCOPES,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "show_dialog": True,
        }

        return f"{settings.SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"

    async def exchange_code(
        self,
        code: str,
    ) -> SpotifyToken:
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }

        response = await self.client.exchange_code(data)

        return SpotifyToken.model_validate(response)

    async def get_current_user(
        self,
        access_token: str,
    ) -> SpotifyUser:
        response = await self.client.get(
            "/me",
            access_token,
        )

        return SpotifyUser.model_validate(response)

    async def get_saved_albums(
        self,
        access_token: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[SpotifyAlbum]:
        response = await self.client.get(
            "/me/albums",
            access_token,
            params={
                "limit": limit,
                "offset": offset,
            },
        )

        albums = [
            SpotifyAlbum.model_validate(item["album"])
            for item in response["items"]
        ]

        return albums
