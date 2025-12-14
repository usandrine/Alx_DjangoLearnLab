from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserProfileSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 
                 'target_id', 'read', 'created_at']
        read_only_fields = ['recipient', 'actor', 'verb', 'target_content_type', 
                           'target_object_id', 'created_at']
    
    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
    
    def get_target_id(self, obj):
        return obj.target_object_id