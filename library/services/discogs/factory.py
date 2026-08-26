import httpx

from .client import DiscogsClient
from .service import DiscogsService


def create_discogs_service() -> DiscogsService:
    client = DiscogsClient(
        httpx.Client()
    )

    return DiscogsService(client)