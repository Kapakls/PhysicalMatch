import asyncio
import traceback

from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from library.models import Album
from library.services.spotify.exceptions import (
    SpotifyAuthorizationCodeMissingError,
    SpotifyAuthorizationError,
    SpotifyConfigurationError,
)
from library.services.spotify.schemas.user import SpotifyUser
from library.services.spotify.service import SpotifyService

from .services.music_matcher.factory import create_music_service
from .services.spotify.factory import create_spotify_service
from .services.user.service import get_or_create_user


def index(request):
    return render(request, "library/index.html")


def login(request):
    try:
        spotify: SpotifyService = create_spotify_service()

        authorization_url = spotify.get_authorization_url()

        return redirect(authorization_url)

    except SpotifyConfigurationError as exc:
        request.session["error_message"] = str(exc)

        if settings.DEBUG:
            request.session["error_traceback"] = traceback.format_exc()

        return redirect("error")


def callback(request):
    try:
        if "error" in request.GET:
            raise SpotifyAuthorizationError(request.GET["error"])

        auth_code = request.GET.get("code")

        if not auth_code:
            raise SpotifyAuthorizationCodeMissingError()

        spotify: SpotifyService = create_spotify_service()

        token = asyncio.run(spotify.exchange_code(auth_code))

        request.session["access_token"] = token.access_token
        request.session["refresh_token"] = token.refresh_token

        spotify_user: SpotifyUser = asyncio.run(
            spotify.get_current_user(token.access_token)
        )

        user, _ = get_or_create_user(spotify_user)

        django_login(request, user)

        return redirect("market")

    except (
        SpotifyAuthorizationError,
        SpotifyAuthorizationCodeMissingError,
    ) as exc:
        request.session["error_message"] = str(exc)

        if settings.DEBUG:
            request.session["error_traceback"] = traceback.format_exc()

        return redirect("error")


@login_required
def market(request):
    return render(
        request,
        "library/loading.html",
    )


@login_required
async def market_fetch(request):
    try:
        access_token = request.session.get("access_token")

        if not access_token:
            return redirect("login")

        music_service = create_music_service()

        await music_service.get_users_music(
            request.user,
            access_token,
        )

        return redirect("market_results")

    except Exception as exc:  # noqa: BLE001
        request.session["error_message"] = str(exc)

        if settings.DEBUG:
            request.session["error_traceback"] = traceback.format_exc()

        return redirect("error")


@login_required
def market_results(request):
    albums = list(
        Album.objects.filter(
            users__user=request.user,
        ).prefetch_related(
            "discogs_marketplace_listings",
        )
    )

    return render(
        request,
        "library/market.html",
        {
            "albums": albums,
        },
    )


def error(request):
    message = request.session.pop(
        "error_message",
        "Something went wrong.",
    )

    error_traceback = request.session.pop(
        "error_traceback",
        None,
    )

    return render(
        request,
        "library/error.html",
        {
            "message": message,
            "traceback": error_traceback,
            "debug": settings.DEBUG,
        },
        status=500,
    )
