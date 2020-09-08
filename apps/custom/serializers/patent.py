from rest_framework import serializers

from model.models import Patent


class PatentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patent
        fields = [
            'id', 'name', 'patent_type', 'patent_code', 'publication_number', 'experts'
        ]


class PatentDetailSerializer(serializers.ModelSerializer):
    main_classifications = serializers.ListField(required=False)
    classifications = serializers.ListField(required=False)
    applicants = serializers.ListField()
    inventors = serializers.ListField()

    class Meta:
        model = Patent
        exclude = ['original_id', 'created_at', 'updated_at']
