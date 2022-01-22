from django.urls import path
from . import views

urlpatterns = [
    path('handle/<str:x>', views.app_account_handler),
    path('', views.app_home),
    path('js_requests/<str:service>', views.js_requests),
    path('<str:service>', views.routingFunction)
]
