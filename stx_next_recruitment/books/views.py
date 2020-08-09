import requests
from rest_framework import status, filters
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.core.exceptions import FieldError
from django.views.generic import TemplateView
from books.models import Books
from books.serializers import BooksSerializer, CriteriaSerializer, \
    RawDataSerializer


class InfoView(TemplateView):
    template_name = 'books/info.html'


class DocView(TemplateView):
    template_name = 'books/doc.html'


class SingleBookView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        """ Handles :model:`books.Books` for listing a single object. """
        try:
            book = Books.objects.get(id=kwargs['id'])
        except Books.DoesNotExist:
            return Response(
                {},
                status=status.HTTP_202_ACCEPTED
            )
        else:
            serialized_book = BooksSerializer(book)
            return Response(
                serialized_book.data,
                status=status.HTTP_200_OK
            )


class ListBooksView(GenericAPIView, ListModelMixin):
    serializer_class = BooksSerializer
    trailing_slash = False
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, )
    url = 'https://www.googleapis.com/books/v1/volumes'

    def __init__(self):
        self.error = False
        super(ListBooksView, self).__init__()

    def get_queryset(self):
        queryset = Books.objects.prefetch_related().all()
        self.request.query_params._mutable = True
        if 'sort' in self.request.query_params:
            self.request.query_params['ordering'] = \
                self.request.query_params['sort']

        try:
            for key in self.request.query_params:
                value_list = self.request.query_params.getlist(key)
                if key == 'author' or key == 'authors':
                    for value in value_list:
                        queryset = queryset.filter(authors__name=value[1:-1])
                elif key == 'category' or key == 'categories':
                    for value in value_list:
                        queryset = queryset.filter(
                            categories__name=value[1:-1]
                        )
                elif key == 'title':
                    for value in value_list:
                        queryset = queryset.filter(title=value[1:-1])
                elif key != 'ordering' and key != 'sort':
                    for value in value_list:
                        criterion = {key: value}
                        queryset = queryset.filter(**criterion)

        except(ValueError, AttributeError, KeyError, FieldError):
            self.error = True

        return queryset

    def get(self, request, *args, **kwargs):
        """ Handles :model:`books.Books` for listing a queryset. """
        response = self.list(request, **kwargs)
        if self.error is not False:
            return Response(
                {'error': 'Wrong filtering parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return response

    def post(self, request, *args, **kwargs):
        criterion = CriteriaSerializer(data=request.data)
        if criterion.is_valid():
            records = requests.get(self.url, params=criterion.data).json()
            deserialized_records = RawDataSerializer(
                data=records['items'],
                many=True
            )
            if deserialized_records.is_valid():
                new_books = deserialized_records.save()
                serialized_new_books = BooksSerializer(new_books, many=True)
                return Response(
                    {'saved_books': serialized_new_books.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': 'Sorry, an internal server error'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {'error': 'Wrong body-data format'},
                status=status.HTTP_400_BAD_REQUEST
            )
