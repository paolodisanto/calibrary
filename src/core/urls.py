from django.urls import path

from . import views
#from .views import generate_qr, qr_code_view

urlpatterns = [
    path("", views.index, name="index"),
    #path("detail/", views.detail, name="detail"),
    path('search/', views.search_item, name='search_item'),
    path('search/<str:qr_value>/', views.search_item, name='search_item_with_qr'),

    #path('generate-qr/<str:tag>/', generate_qr, name='generate_qr'),
    #path('qr-code/', qr_code_view, name='qr_code_view'),
]