from django.urls import path
from . import views


app_name = 'books'

urlpatterns = [
    path('info', views.InfoView.as_view(), name='info'),
    path('doc', views.DocView.as_view(), name='doc'),
    path('v1/books/<str:id>', views.SingleBookView.as_view(),
         name='single_book'),
    path('v1/books/', views.ListBooksView.as_view(), name='book_list'),
]
