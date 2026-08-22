import httpx
from django.conf import settings


class SpotifyClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get(
        self,
        endpoint: str,
        access_token: str,
        params: dict | None = None,
    ) -> dict:
        response = await self.client.get(
            f"{settings.SPOTIFY_API_URL}{endpoint}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params=params,
        )

        response.raise_for_status()

        return response.json()

    async def exchange_code(
        self,
        data: dict,
    ) -> dict:
        response = await self.client.post(
            settings.SPOTIFY_TOKEN_URL,
            data=data,
        )

        response.raise_for_status()

        return response.json()
