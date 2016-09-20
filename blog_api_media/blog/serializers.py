from rest_framework import serializers

from blog.models import User, Entry, Blog


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'accesskey', 'password',
                  'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class BlogSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'


class EntrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'
