from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination parameters for API requests."""

    limit: int = Field(default=50, ge=1, le=50)
    offset: int = Field(default=0, ge=0)

class SpotifyToken(BaseModel):
    """Represents an OAuth access token response from Spotify."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None
    scope: str