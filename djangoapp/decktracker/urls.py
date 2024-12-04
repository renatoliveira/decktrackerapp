from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # decks
    path('decks/<int:deck_id>/', views.view_deck, name='view_deck'),
    path('decks/', views.view_my_decks, name='view_my_decks'),
    path('decks/new', views.create_a_deck, name='create_a_deck'),
    path('decks/<int:deck_id>/delete', views.remove_a_deck, name='delete_a_deck'),

    # registration
    path('register/', views.register_view, name='register'),
    path('user/register', views.register_view, name='register'),
    path('user/login', views.login_view, name='login'),
    path('user/logout', views.logout_view, name='logout'),
]