from rest_framework import serializers

from model.models import Periodical


class PeriodicalListSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(required=False)
    foundations = serializers.ListField(required=False)

    class Meta:
        model = Periodical
        fields = [
            'id', 'title', 'doi', 'first_creator', 'periodical_name', 'foundations', 'keywords'
        ]


class PeriodicalDetailSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(required=False)
    foundations = serializers.ListField(required=False)
    creators = serializers.ListField(required=False)
    organizations = serializers.ListField(required=False)
    classification = serializers.ListField(required=False)

    class Meta:
        model = Periodical
        exclude = [
            'original_id', 'created_at', 'updated_at'
        ]
