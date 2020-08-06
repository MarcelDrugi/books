from django.views.generic import TemplateView
from rest_framework import status, filters
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from books.models import Books
from books.serializers import BooksSerializer


class InfoView(TemplateView):
    template_name = 'books/info.html'


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
            print(serialized_book.data)
            return Response(
                serialized_book.data,
                status=status.HTTP_200_OK
            )


class ListBooksView(GenericAPIView, ListModelMixin):
    serializer_class = BooksSerializer
    trailing_slash = False
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)

    def __init__(self):
        self.errors = []
        super(ListBooksView, self).__init__()

    def get_queryset(self):
        queryset = Books.objects.prefetch_related().all()
        self.request.query_params._mutable = True
        if 'sort' in self.request.query_params:
            self.request.query_params['ordering'] = \
                self.request.query_params['sort']

        for key in self.request.query_params:
            value_list = self.request.query_params.getlist(key)
            if key == 'author' or key == 'authors':
                for value in value_list:
                    queryset = queryset.filter(authors__name=value[1:-1])
            elif key == 'category' or key == 'categories':
                for value in value_list:
                    queryset = queryset.filter(categories__name=value[1:-1])
            elif key == 'title':
                for value in value_list:
                    queryset = queryset.filter(title=value[1:-1])
            else:
                for value in value_list:
                    criterion = {key: value}
                    queryset = queryset.filter(**criterion)

        return queryset

    def get(self, request, *args, **kwargs):
        """ Handles :model:`books.Books` for listing a queryset. """
        response = self.list(request, **kwargs)

        if not self.errors:
            return response
        else:
            return Response(
                {'errors': self.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
