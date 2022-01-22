from django.urls import path
from . import views

urlpatterns = [
    path('', views.gotoHome),
    path('home/', views.home),
    path('contact/', views.contact_page),
    path('downloads/', views.download_page),
    path('guide/', views.guide_page),
    path('share-pass/', views.sharepass_page),
    path('account/', views.account_page)
]
