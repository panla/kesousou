# -*- encoding=utf-8 -*-

from rest_framework import serializers

from model.models import Expert


class ExpertListSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(required=False)

    class Meta:
        model = Expert
        fields = [
            'id', 'name', 'organization', 'department', 'post', 'title', 'keywords', 'info_link'
        ]


class ExpertDetailSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(required=False)

    class Meta:
        model = Expert
        fields = '__all__'
