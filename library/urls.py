from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("market/", views.market, name="market"),
    path("market/fetch/", views.market_fetch, name="market_fetch"),
    path("market/results/", views.market_results, name="market_results"),
    path("error/", views.error, name="error"),
]