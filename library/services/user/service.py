from library.models import User
from library.services.spotify.schemas.user import SpotifyUser


def get_or_create_user(spotify_user: SpotifyUser) -> tuple[User, bool]:
    user_data = {
        "username": spotify_user.id,
        "display_name": spotify_user.display_name or "",
        "country": spotify_user.country or "",
        "profile_url": (
            spotify_user.external_urls.spotify
            if spotify_user.external_urls
            else ""
        ),
        "profile_image": (
            spotify_user.images[0].url
            if spotify_user.images
            else "https://i.scdn.co/image/ab6761610000e5eb55d39ab9c21d506aa52f7021"
        ),
    }

    return User.objects.get_or_create(
        spotify_id=spotify_user.id,
        defaults=user_data,
    )