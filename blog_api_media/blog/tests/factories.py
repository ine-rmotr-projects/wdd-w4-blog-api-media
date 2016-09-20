import factory
from factory.fuzzy import FuzzyInteger, FuzzyDecimal

from blog.models import Blog, Entry


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog

    name = factory.Sequence(lambda n: 'Blog {0}'.format(n + 1))
    tagline = 'Some tagline'


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    blog = factory.SubFactory(BlogFactory)
    headline = 'Some headline'
    body_text = 'Some body text'
    number_comments = FuzzyInteger(100)
    scoring = FuzzyDecimal(0.00, 9.99)
