class SpotifyAuthorizationError(Exception):
    def __init__(self, error: str):
        self.error = error
        super().__init__(f"Spotify authorization failed: {error}")


class SpotifyAuthorizationCodeMissingError(Exception):
    def __init__(self):
        super().__init__("No Spotify authorization code received.")


class SpotifyConfigurationError(Exception):
    pass
