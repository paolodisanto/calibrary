from django.urls import path

from . import views
#from .views import generate_qr, qr_code_view

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/", views.detail, name="detail"),
    #path('generate-qr/<str:tag>/', generate_qr, name='generate_qr'),
    #path('qr-code/', qr_code_view, name='qr_code_view'),
]