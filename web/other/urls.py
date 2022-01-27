from django.urls import path
from . import views

urlpatterns = [
    path('', views.gotoHome),
    path('home/', views.home),
    path('share-pass/', views.sharepass),
    path('<str:service>/', views.allRoutesHandler)
]
