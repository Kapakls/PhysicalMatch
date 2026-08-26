from pydantic import BaseModel


class SpotifyExternalUrls(BaseModel):
    """Contains external URLs associated with a Spotify resource."""

    spotify: str


class SpotifyImage(BaseModel):
    """Represents an image associated with a Spotify resource."""

    url: str
    height: int | None = None
    width: int | None = None


class SpotifyExplicitContent(BaseModel):
    """Represents the user's explicit content settings on Spotify."""

    filter_enabled: bool
    filter_locked: bool


class SpotifyFollowers(BaseModel):
    """Represents follower information for a Spotify user."""

    href: str | None
    total: int


class SpotifyUser(BaseModel):
    """Represents a Spotify user and their profile information."""

    account_id: str
    country: str | None = None
    display_name: str | None = None
    email: str | None = None
    explicit_content: SpotifyExplicitContent
    external_urls: SpotifyExternalUrls
    followers: SpotifyFollowers
    href: str
    id: str
    images: list[SpotifyImage]
    product: str
    type: str
    uri: str