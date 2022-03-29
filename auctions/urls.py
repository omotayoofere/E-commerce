from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-list", views.create_listing, name="create-list"),
    path("create-list/<int:pk>", views.auction_details, name="create-list")
]
