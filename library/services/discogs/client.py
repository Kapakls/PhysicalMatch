import httpx
from django.conf import settings

from .exceptions import DiscogsError


class DiscogsClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:
        response = await self.client.get(
            f"{settings.DISCOGS_API_URL}{endpoint}",
            params=params,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DiscogsError(
                f"Discogs API request failed with status "
                f"{response.status_code}"
            ) from exc

        return response.json()