import httpx

from .client import DiscogsClient
from .service import DiscogsService


def create_discogs_service() -> DiscogsService:
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0),
    )
    
    client = DiscogsClient(http_client)

    return DiscogsService(client)
