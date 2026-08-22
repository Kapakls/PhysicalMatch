from pydantic import BaseModel


class SpotifyExternalUrls(BaseModel):
    spotify: str


class SpotifyImage(BaseModel):
    url: str
    height: int | None = None
    width: int | None = None


class SpotifyExplicitContent(BaseModel):
    filter_enabled: bool
    filter_locked: bool


class SpotifyFollowers(BaseModel):
    href: str | None
    total: int


class SpotifyUser(BaseModel):
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