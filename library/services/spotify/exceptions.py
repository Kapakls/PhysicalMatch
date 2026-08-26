class SpotifyError(Exception):
    """Base exception for Spotify-related errors."""


class SpotifyAuthorizationError(SpotifyError):
    """Raised when Spotify authorization fails."""

    def __init__(self, error: str):
        self.error = error
        super().__init__(f"Spotify authorization failed: {error}")


class SpotifyAuthorizationCodeMissingError(SpotifyError):
    """Raised when no Spotify authorization code is provided."""

    def __init__(self):
        super().__init__("No Spotify authorization code received")


class SpotifyConfigurationError(SpotifyError):
    """Raised when the Spotify service is incorrectly configured."""