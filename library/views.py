from django.shortcuts import redirect, render


def index(request):
    return render(request, "library/index.html")

def login(request):
    print("You are now logged in.")
    return redirect("index")