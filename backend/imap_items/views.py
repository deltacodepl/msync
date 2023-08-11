from rest_framework import viewsets

from .serializers import ImapItemSerializer
from .models import ImapItem


class ImapItemViewSet(viewsets.ModelViewSet):
    queryset = ImapItem.objects.all().order_by('-date_uploaded')
    serializer_class = ImapItemSerializer
