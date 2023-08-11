from rest_framework import serializers
from .models import ImapItem


class ImapItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImapItem
        fields = '__all__'
        read_only_fields = ("id", )
