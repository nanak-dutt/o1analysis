from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserSerializer(serializers.Serializer):
	name = serializers.CharField(max_length = 100)
	email = serializers.EmailField()
	college = serializers.CharField(max_length = 100)
	key = serializers.CharField(max_length=100)
	mobile = serializers.IntegerField()

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()

class CollegeRankListSerializer(serializers.Serializer):
    college = serializers.CharField(max_length=100)