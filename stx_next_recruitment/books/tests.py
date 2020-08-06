"""
API-views tests.
Although it's hard to call them unit tests, because their functionality is
closely related to manually created serializers, but they help to control
the application operation.
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from books.models import Authors
from books.models import Categories, Books


class GetBooksViewAPITestCase(APITestCase):
    def setUp(self):
        self.author = Authors.objects.create(name='Jan Kowalski')
        self.category = Categories.objects.create(name='History')

        book_1_data = {
            'id': 'abcd1234',
            'title': 'Some Title',
            'published_date': 2015,
            'average_rating': 4.5,
            'ratings_count': 28,
            'thumbnail': 'some/path/to/img.png'
        }
        book_2_data = {
            'id': '54321bbb',
            'title': 'Other Title',
            'published_date': 1955,
            'average_rating': 3.0,
            'ratings_count': 194,
            'thumbnail': 'other/path/to/img.png'
        }

        self.book_1 = Books.objects.create(**book_1_data)
        self.book_1.authors.add(self.author)
        self.book_1.categories.add(self.category)
        self.book_1.save()

        self.book_2 = Books.objects.create(**book_2_data)
        self.book_2.authors.add(self.author)
        self.book_2.categories.add(self.category)
        self.book_2.save()

    def test_list(self):
        url = reverse('books:book_list')

        # full list
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(response.data[0]['id'], self.book_1.id)
        self.assertTrue(response.data[1]['id'], self.book_2.id)

        # filter request
        response = self.client.get(
            url + '?title=' + '"' + self.book_1.title + '"'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data[0]['id'], self.book_1.id)

        response = self.client.get(
            url + '?author=' + '"' + self.author.name + '"'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(
            response.data[0]['average_rating'],
            self.book_1.average_rating
        )
        self.assertTrue(
            response.data[1]['average_rating'],
            self.book_2.average_rating
        )

    def test_single_book(self):
        url = reverse('books:single_book', kwargs={'id': self.book_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.book_2.id)
        self.assertEqual(response.data['title'], self.book_2.title)


class PostBooksViewAPITestCase(APITestCase):

    def test_post_data(self):
        """ Results depend on an external source! """
        body = {
            'q': 'war'
        }
        response = self.client.post(reverse('books:db'), body)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(len(response.data['saved_books'][0]), 8)


class InfoViewTestCase(TestCase):
    """ Test of the info-page """
    def test_info_view(self):
        response = Client().get(reverse('books:info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/info.html')


class DocViewTestCase(TestCase):
    """ Test of page with API documentation """
    def test_doc_view(self):
        response = Client().get(reverse('books:doc'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/doc.html')
