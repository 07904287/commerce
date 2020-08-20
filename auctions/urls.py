from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<str:id>", views.listing, name="listing"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("watchlist/<str:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:id>", views.specific_category, name="specific_category"),
    path("close/<str:id>", views.close, name="close"),
]
