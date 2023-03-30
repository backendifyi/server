from rest_framework import serializers
from .models import EmailModel

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return EmailModel.objects.create(**validated_data)