from decimal import Decimal

from pydantic import BaseModel


class MarketplaceListing(BaseModel):
    """Represents a Discogs marketplace listing."""

    title: str
    price: Decimal
    currency: str
    listing_id: str
    listing_url: str
    seller_country: str
    media_condition: str
    sleeve_condition: str
    seller_rating: Decimal


class MarketplaceSearchResponse(BaseModel):
    """Represents the response returned by a marketplace search."""

    listings: list[MarketplaceListing]