from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Following


User = get_user_model()


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request', None).user
        if not user.is_authenticated:
            return False
        return Following.objects.filter(follower=user, author=obj).exists()