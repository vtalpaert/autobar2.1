from rest_framework import serializers

from robotcocktail.artists.models import FollowRequest


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = ["id", "from_profile", "to_profile", "status", "message"]
