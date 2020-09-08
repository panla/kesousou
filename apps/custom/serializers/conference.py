from rest_framework import serializers

from model.models import Conference


class ConferenceListSerializer(serializers.ModelSerializer):
    sponsors = serializers.ListField(required=False)
    classifications = serializers.ListField(required=False)

    class Meta:
        model = Conference
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
        model = Conference
        exclude = [
            'original_id', 'created_at', 'updated_at'
        ]
