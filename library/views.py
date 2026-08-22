from django.shortcuts import redirect, render

from .services.spotify.factory import create_spotify_service


def index(request):
    return render(request, "library/index.html")


def login(request):
    spotify = create_spotify_service()

    authorization_url = spotify.get_authorization_url()

    return redirect(authorization_url)


def callback(request):
    code = request.GET.get("code")

    print("Spotify login Code:", code)

    return redirect("index")
