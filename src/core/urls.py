from django.urls import path
from . import views
from .views import instrument_detail


urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search_item, name='search_item'),
    path('search/<str:qr_value>/', views.search_item, name='search_item_with_qr'),
    path('instrument/<str:tag_id>/', instrument_detail, name='instrument_detail'),
    path('delete_attachment/<int:attachment_id>/', views.delete_attachment, name='delete_attachment'),
]