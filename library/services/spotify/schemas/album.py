from pydantic import BaseModel


class SpotifyExternalUrls(BaseModel):
    """Contains external URLs associated with a Spotify resource."""

    spotify: str


class SpotifyImage(BaseModel):
    """Represents an image associated with a Spotify resource."""

    url: str
    height: int | None = None
    width: int | None = None


class SpotifyArtist(BaseModel):
    """Represents a Spotify artist."""

    external_urls: SpotifyExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class SpotifyCopyright(BaseModel):
    """Represents copyright information for a Spotify resource."""

    text: str
    type: str


class SpotifyExternalIds(BaseModel):
    """Contains external identifiers associated with a Spotify resource."""

    upc: str | None = None


class SpotifyTrack(BaseModel):
    """Represents a Spotify track."""

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
    """Represents a paginated collection of Spotify tracks."""

    href: str
    limit: int
    next: str | None
    offset: int
    previous: str | None
    total: int
    items: list[SpotifyTrack]


class SpotifyAlbum(BaseModel):
    """Represents a Spotify album and its associated metadata."""

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


class SpotifySavedAlbum(BaseModel):
    """Represents an album saved in a user's Spotify library."""

    album: SpotifyAlbum


class SpotifyGetAlbumsResponse(BaseModel):
    """Represents the response returned when retrieving a user's saved albums."""

    items: list[SpotifySavedAlbum]
