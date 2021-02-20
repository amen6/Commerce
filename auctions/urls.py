from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("list/<str:list>", views.list_view, name="list_view"),
    path("addwatchlist/<str:list>", views.add_watchlist, name="addwatchlist"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("categories/<str:category>", views.category_view, name="category_view"),
    path("close/<str:list>", views.close, name="close"),
    path("delete/<str:list>", views.delete, name="delete"),
    path("addbid/<str:list>", views.take_bid, name="addbid"),
    path("addcomment/<str:list>", views.addcomment, name="comment")
]
