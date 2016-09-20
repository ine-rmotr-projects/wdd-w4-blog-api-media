from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


def validate_authkey(value):
    """Raises a ValidationError if value has not length 32"""
    if not len(value) == 32:
        raise ValidationError(
            'Value must be a string containing 32 alphanumeric characters')


class User(AbstractUser):

    accesskey = models.CharField(max_length=32, unique=True,
                                 validators=[validate_authkey])
    secretkey = models.CharField(max_length=32,
                                 validators=[validate_authkey])

    def __unicode__(self):
        return self.username

    __str__ = __unicode__


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    users = models.ManyToManyField(User)
    number_comments = models.IntegerField()
    scoring = models.DecimalField(max_digits=3, decimal_places=2)
    image = models.ImageField(upload_to='images', max_length=254,
                              null=True, blank=True)

    def __unicode__(self):
        return self.headline

    __str__ = __unicode__
