from django.urls import path
from . import views


app_name = 'books'

urlpatterns = [
    path('info', views.InfoView.as_view(), name='info'),
]
