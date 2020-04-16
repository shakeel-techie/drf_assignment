from rest_framework.serializers import ModelSerializer
from document import models


class DocumentSerializer(ModelSerializer):

    class Meta:
        model = models.Document
        fields = '__all__'
