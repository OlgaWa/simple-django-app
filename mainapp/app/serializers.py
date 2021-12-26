from rest_framework import serializers
from .models import User, Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email',
                  'street', 'suite', 'city', 'zipcode',
                  'lat', 'lng', 'phone', 'website',
                  'company_name', 'catch_phrase', 'company_bs')


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'userId', 'title', 'completed')
