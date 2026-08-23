import asyncio

from django.contrib.auth import login as django_login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from library.services.spotify.schemas.user import SpotifyUser

from .services.spotify.factory import create_spotify_service
from .services.user.service import get_or_create_user


def index(request):
    return render(request, "library/index.html")


def login(request):
    spotify = create_spotify_service()

    authorization_url = spotify.get_authorization_url()

    return redirect(authorization_url)


def callback(request):
    if "error" in request.GET:
        return HttpResponseBadRequest(
            f"Spotify authorization failed: {request.GET['error']}"
        )

    auth_code = request.GET.get("code")

    if not auth_code:
        return HttpResponseBadRequest("No Spotify authorization code received")
    
    spotify = create_spotify_service()

    token = asyncio.run(
        spotify.exchange_code(auth_code)
    )

    request.session["access_token"] = token.access_token
    request.session["refresh_token"] = token.refresh_token

    spotify_user: SpotifyUser = asyncio.run(
        spotify.get_current_user(token.access_token)
    )

    user, _ = get_or_create_user(spotify_user)

    django_login(request, user)

    return redirect("index")