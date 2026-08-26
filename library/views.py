import asyncio
import traceback

from django.conf import settings
from django.contrib.auth import login as django_login
from django.shortcuts import redirect, render

from library.services.spotify.exceptions import (
    SpotifyAuthorizationCodeMissingError,
    SpotifyAuthorizationError,
    SpotifyConfigurationError,
)
from library.services.spotify.schemas.user import SpotifyUser
from library.services.spotify.service import SpotifyService

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

        return redirect("index")

    except (
        SpotifyAuthorizationError,
        SpotifyAuthorizationCodeMissingError,
    ) as exc:
        request.session["error_message"] = str(exc)

        if settings.DEBUG:
            request.session["error_traceback"] = traceback.format_exc()

        return redirect("error")


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
