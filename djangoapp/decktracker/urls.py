from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deck/<int:deck_id>/', views.view_deck, name='view_deck'),
    path('register/', views.register_view, name='register'),
    path('user/register', views.register_view, name='register'),
    path('user/login', views.login_view, name='login'),
]