from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:deck_id>/', views.view_deck, name='view_deck'),
]