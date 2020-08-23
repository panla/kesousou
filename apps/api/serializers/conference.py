# -*- encoding=utf-8 -*-

from rest_framework import serializers

from model.models import Conferences


class ConferenceListSerializer(serializers.ModelSerializer):
    sponsors = serializers.ListField(required=False)
    classifications = serializers.ListField(required=False)

    class Meta:
        model = Conferences
        fields = [
            'id', 'title', 'first_creator', 'sponsors', 'classifications', 'experts'
        ]


class ConferenceDetailSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(required=False)
    creators = serializers.ListField()
    organizations = serializers.ListField()
    sponsors = serializers.ListField(required=False)
    classifications = serializers.ListField(required=False)

    class Meta:
        model = Conferences
        exclude = [
            'original_id', 'created_at', 'updated_at'
        ]
