from unittest.util import _MAX_LENGTH
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class RankListSerializer(serializers.Serializer):
    college = serializers.CharField(max_length=100)