from rest_framework import serializers
from .models import EmailModel

class EmailSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = EmailModel
        fields = [
            'id',
            'email_address',
            'date',
            'time',
            'total_request',
            'is_valid',
            'syntax_error_status',
            'role_status',
            'disposable_status',
            'free_status',
            'dns_status',
            'role',
            'disposable_provider',
            'domain',
            'account',
        ]

    def get_date(self, obj):
        return str(obj.time_added)[:10]

    def get_time(self, obj):
        return str(obj.time_added)[11:16]

class AllEmailSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='emailbox.project.name')

    class Meta:
        model = EmailModel
        fields = [
            'id',
            'email_address',
            'date',
            'time',
            'total_request',
            'project_name',
            'is_valid',
            'syntax_error_status',
            'role_status',
            'disposable_status',
            'free_status',
            'dns_status',
            'role',
            'disposable_provider',
            'domain',
            'account',
        ]

    def get_date(self, obj):
        return str(obj.time_added.date())

    def get_time(self, obj):
        return str(obj.time_added.time())