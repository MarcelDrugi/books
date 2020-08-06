from rest_framework import serializers
from books.models import Authors, Categories, Books


class AuthorsSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
        return value.name

    class Meta:
        model = Authors
        fields = ['name']


class CategoriesSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
        return value.name

    class Meta:
        model = Categories
        fields = ['name']


class BooksSerializer(serializers.ModelSerializer):
    authors = AuthorsSerializer(many=True)
    categories = CategoriesSerializer(many=True)

    class Meta:
        model = Books
        fields = '__all__'
