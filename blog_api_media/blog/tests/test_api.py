# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import date

from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import User
from .factories import *


class EntryTestCase(APITestCase):

    def setUp(self):
        super(EntryTestCase, self).setUp()
        self.blog = BlogFactory()
        self.user = User.objects.create_user(
            username='larrypage', password='abc123', first_name='Larry',
            last_name='Page', email='lpage@google.com', accesskey='a' * 32,
            secretkey='b' * 32)

        self.entry = EntryFactory(
            blog=self.blog, scoring=2.04, number_comments='10')
        self.entry.users.add(self.user)
        self.entry.pub_date = date(2016, 1, 15)
        self.entry.save()

        self.entry_2 = EntryFactory(
            blog=self.blog, scoring=4.25, number_comments='20')
        self.entry_2.pub_date = date(2016, 1, 15)
        self.entry_2.save()

    def tearDown(self):
        cache.clear()

    def test_version(self):
        """Should return API version when GETing /status endpoint"""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'version': 'v1'})

    def test_format_xml(self):
        """Should return XML response when format=xml param is given"""
        params = {'format': 'xml'}
        response = self.client.get('/api/v1/entries', params)
        xml_content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.accepted_media_type, 'application/xml')
        self.assertTrue(xml_content.startswith(
            '<?xml version="1.0" encoding="utf-8"?>'))

    def test_format_json(self):
        """Should return JSON response when format=json param is given"""
        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'blog': 'http://testserver/api/v1/blogs/1?format=json',
                    'body_text': 'Some body text',
                    'headline': 'Some headline',
                    'image': None,
                    'mod_date': '2016-09-20',
                    'number_comments': 10,
                    'pub_date': '2016-01-15',
                    'scoring': '2.04',
                    'url': 'http://testserver/api/v1/entries/1?format=json',
                    'users': [
                        'http://testserver/api/v1/users/1?format=json'
                    ]
                },
                {
                    'blog': 'http://testserver/api/v1/blogs/1?format=json',
                    'body_text': 'Some body text',
                    'headline': 'Some headline',
                    'image': None,
                    'mod_date': '2016-09-20',
                    'number_comments': 20,
                    'pub_date': '2016-01-15',
                    'scoring': '4.25',
                    'url': 'http://testserver/api/v1/entries/2?format=json',
                    'users': []
                }
            ]
        }
        params = {'format': 'json'}
        response = self.client.get('/api/v1/entries', params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.accepted_media_type, 'application/json')
        self.assertEqual(response.json(), expected)

    def test_format_json_default(self):
        """Should return JSON response by default when no format param is given"""
        response = self.client.get('/api/v1/entries')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.accepted_media_type, 'application/json')

    def test_throttling(self):
        """Should allow up to 50 request per minute for authenticated user"""
        for i in range(50):
            response = self.client.get('/api/v1/entries')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/v1/entries')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertTrue('Request was throttled.' in response.json()['detail'])

    def test_entry_image_upload(self):
        """Should create an Entry with an image attached"""
        self.assertEqual(Entry.objects.count(), 2)
        filepath = os.path.join(settings.BASE_DIR,
                                'blog/tests/fixtures/python-logo.png')
        with open(filepath, 'rb') as image_file:
            payload = {
                'blog': 'http://testserver/api/v1/blogs/1',
                'users': ['http://testserver/api/v1/users/1'],
                'headline': 'New entry',
                'body_text': 'Some body text',
                'number_comments': 15,
                'scoring': 4.25,
                'image': image_file
            }
            response = self.client.post(
                '/api/v1/entries', payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 3)
        entry = Entry.objects.get(headline='New entry')
        self.assertTrue(entry.image.url.startswith('/media/images/python-logo'))
