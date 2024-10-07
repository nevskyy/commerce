from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings_by_category", views.show_active_listings_by_category, name="listings_by_category"),
    path("listing/<int:listing_id>", views.select_listing, name="select_listing"),
    path("remove_listing/<int:listing_id>", views.remove_listing, name="remove_listing"),
    path("add_listing/<int:listing_id>", views.add_listing, name="add_listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watch_list", views.show_watch_list, name="watch_list"),
    
]
