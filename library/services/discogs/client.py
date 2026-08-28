import httpx
from django.conf import settings


class DiscogsClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:
        response = await self.client.get(
            f"{settings.DISCOGS_MARKETPLACE_API_URL}{endpoint}",
            params=params,
        )

        return response.json()
