from unittest.util import _MAX_LENGTH
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
	Name = serializers.CharField(max_length = 100)
	Email = serializers.EmailField()
	College = serializers.CharField(max_length = 100)
	Key = serializers.CharField(max_length=100)

class UserLoginSerializer(serializers.Serializer):
	Email = serializers.EmailField()
	College = serializers.CharField(max_length = 100)
	Key = serializers.CharField(max_length=100)
