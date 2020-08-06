from django.urls import path
from django.views.decorators.http import require_GET, require_POST
from . import views


app_name = 'books'

urlpatterns = [
    path('', views.InfoView.as_view(), name='info'),
    path('doc', views.DocView.as_view(), name='doc'),
    path('v1/books/<str:id>', require_GET(views.SingleBookView.as_view()),
         name='single_book'),
    path('v1/books', require_GET(views.ListBooksView.as_view()),
         name='book_list'),
    path('v1/db', require_POST(views.ListBooksView.as_view()), name='db'),
]
