from rest_framework import serializers

from model.models import Achievement


class AchievementListSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField()
    trade_name = serializers.ListField(required=False)
    class Meta:
        model = Achievement
        fields = [
            'id', 'sn', 'title', 'keywords', 'trade_name', 'level'
        ]


class AchievementDetailSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(required=False)
    organizations = serializers.ListField(required=False)
    creators = serializers.ListField(required=False)
    trade_name = serializers.ListField(required=False)

    class Meta:
        model = Achievement
        exclude = [
            'original_id', 'created_at', 'updated_at'
        ]
