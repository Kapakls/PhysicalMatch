from library.models import Album
from library.services.discogs.client import DiscogsClient
from library.services.discogs.schemas.marketplace import (
    MarketplaceListing,
    MarketplaceSearchResponse,
)


class DiscogsService:
    """Provides application-level operations for Discogs Marketplace listing data."""

    MATCH_THRESHOLD = 0.1

    def __init__(self, client: DiscogsClient):
        self.client = client

    async def search_marketplace(
        self,
        album: Album,
    ) -> list[MarketplaceListing]:
        response = await self.client.get(
            "/marketplace/match",
            params={
                "artist": album.artist,
                "album": album.title,
                "threshold": self.MATCH_THRESHOLD,
            },
        )

        data = MarketplaceSearchResponse.model_validate(response)

        return data.listings