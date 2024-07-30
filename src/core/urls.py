from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search_item, name='search_item'),
    path('search/<str:qr_value>/', views.search_item, name='search_item_with_qr'),
]