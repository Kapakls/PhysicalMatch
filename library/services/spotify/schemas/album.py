from pydantic import BaseModel


class SpotifyExternalUrls(BaseModel):
    spotify: str


class SpotifyImage(BaseModel):
    url: str
    height: int | None = None
    width: int | None = None


class SpotifyArtist(BaseModel):
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class SpotifyCopyright(BaseModel):
    text: str
    type: str


class SpotifyExternalIds(BaseModel):
    upc: str | None = None


class SpotifyTrack(BaseModel):
    artists: list[SpotifyArtist]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    name: str
    track_number: int
    type: str
    uri: str
    is_local: bool


class SpotifyTracks(BaseModel):
    href: str
    limit: int
    next: str | None
    offset: int
    previous: str | None
    total: int
    items: list[SpotifyTrack]


class SpotifyAlbum(BaseModel):
    album_type: str
    total_tracks: int
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    images: list[SpotifyImage]
    name: str
    release_date: str
    release_date_precision: str
    type: str
    uri: str
    artists: list[SpotifyArtist]
    tracks: SpotifyTracks
    copyrights: list[SpotifyCopyright]
    external_ids: SpotifyExternalIds
    genres: list[str]