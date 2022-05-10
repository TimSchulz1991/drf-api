from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    # validation function convention: validate_field-to-validate
    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2: # 2Mb
            raise serializers.ValidationError(
                "Image size larger than 2MB!"
            )
        if value.image.width > 4096: # px
            raise serializers.ValidationError(
                "Image too large (larger than 4096px in width)!"
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                "Image too large (larger than 4096px in height)!"
            )
        return value


    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content',
            'image', 'is_owner', 'profile_id', 'profile_image', 'image_filter'
        ]

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
