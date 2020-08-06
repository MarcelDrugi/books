from contextlib import suppress

from django.db import transaction
from rest_framework import serializers
from books.models import Authors, Categories, Books
from rest_framework.exceptions import ValidationError


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


class CriteriaSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=512)


class RawDataSerializer(serializers.Serializer):
    """
    I didn't know which fields should be required, so I assumed only id
    was required.
    """
    id = serializers.CharField(max_length=32)
    title = serializers.CharField(max_length=256, required=False)
    authors = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    published_date = serializers.CharField(max_length=4, required=False)
    categories = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    average_rating = serializers.FloatField(required=False)
    ratings_count = serializers.IntegerField(required=False)
    thumbnail = serializers.CharField(required=False)

    def to_internal_value(self, data):
        try:
            adapted = {'id': data['id']}
        except KeyError:
            raise ValidationError('Wrong raw-data format')
        with suppress(KeyError):
            adapted['title'] = data['volumeInfo']['title']
        with suppress(KeyError):
            adapted['authors'] = data['volumeInfo']['authors']
        with suppress(KeyError):
            adapted['published_date'] = data['volumeInfo']['publishedDate'][:4]
        with suppress(KeyError):
            adapted['categories'] = data['volumeInfo']['categories']
        with suppress(KeyError):
            adapted['average_rating'] = data['volumeInfo']['averageRating']
        with suppress(KeyError):
            adapted['ratings_count'] = data['volumeInfo']['ratingsCount']
        with suppress(KeyError):
            adapted['thumbnail'] = data['volumeInfo']['imageLinks']['thumbnail']
        return super(RawDataSerializer, self).to_internal_value(adapted)

    def create(self, validated_data):
        with transaction.atomic():
            authors = validated_data.pop('authors', [])
            categories = validated_data.pop('categories', [])
            try:
                book = Books.objects.get(id=validated_data['id'])
                for key, value in validated_data.items():
                    setattr(book, key, value)
                book.save()
            except AttributeError:
                raise ValidationError('wrong data')
            except Books.DoesNotExist:
                book = Books.objects.create(**validated_data)

            for name in categories:
                try:
                    category = Categories.objects.get(name=name)
                except Categories.DoesNotExist:
                    category = Categories.objects.create(name=name)
                book.categories.add(category)

            for name in authors:
                try:
                    author = Authors.objects.get(name=name)
                except Authors.DoesNotExist:
                    author = Authors.objects.create(name=name)
                book.authors.add(author)
        return book
