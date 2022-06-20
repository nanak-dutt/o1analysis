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
	college = serializers.CharField(max_length = 100)
	key = serializers.CharField(max_length=100)

class CollegeRankListSerializer(serializers.Serializer):
    college = serializers.CharField(max_length=100)

class AnalysisSerializer(serializers.Serializer):
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)

class ranklistSerializer(serializers.Serializer):
	email = serializers.EmailField()
	rank_subject = serializers.CharField(max_length = 100)