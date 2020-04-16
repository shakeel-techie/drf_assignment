from rest_framework import viewsets, permissions

from document.serializers import DocumentSerializer
from document.models import Document


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
