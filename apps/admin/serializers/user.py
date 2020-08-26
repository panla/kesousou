from django.contrib.auth.views import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.get('password')
        if password:
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
        else:
            raise Exception('there is no password')

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'password', 'is_superuser', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
