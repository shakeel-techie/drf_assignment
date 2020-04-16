import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from document.models import Document
from document.serializers import DocumentSerializer

client = Client()


class GetAllDocumentsTest(TestCase):
    """ Test module for GET all puppies API """
    username = "test"
    email = "test@xyz.com"
    password = "Test123!"

    def setUp(self):
        user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.pdf_doc = Document.objects.create(
            type='PDF', source_type='S1', input_meta_data={"meta": "PDF file"}, owner=user)
        Document.objects.create(
            type='CSV', source_type='S2', input_meta_data={"meta": "CSV file"}, owner=user)
        Document.objects.create(
            type='XML', source_type='S1', input_meta_data={"meta": "XML file"}, owner=user)
        client.login(username=self.username, password=self.password)

    def test_get_all_documents(self):
        # get API response
        response = client.get(reverse('doc-list'))
        # get data from db
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_document(self):
        response = client.get(
            reverse('doc-detail', kwargs={'pk': self.pdf_doc.pk}))
        document = Document.objects.get(pk=self.pdf_doc.pk)
        serializer = DocumentSerializer(document)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_document(self):
        response = client.get(
            reverse('doc-detail', kwargs={'pk': 21}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewDocumentTest(TestCase):
    """ Test module for inserting a new document """
    username = "test"
    email = "test@xyz.com"
    password = "Test123!"

    def setUp(self):
        user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.valid_payload = {
            "type": "PDF",
            "source_type": "S1",
            "input_meta_data": {
                "test1": 1
            },
            "owner": user.pk
        }
        client.login(username=self.username, password=self.password)

        self.invalid_payload = {
            "type": "PDF",
            "source_type": "S3",  # Invalid choice
            "input_meta_data": {
                "test1": 1
            },
            "owner": user.pk
        }

    def test_create_valid_document(self):
        response = client.post(
            reverse('doc-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_document(self):
        response = client.post(
            reverse('doc-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleDocumentTest(TestCase):
    """ Test module for updating an existing document """
    username = "test"
    email = "test@xyz.com"
    password = "Test123!"
    client.login(username=username, password=password)

    def setUp(self):
        user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.pdf_doc = Document.objects.create(
            type='PDF', source_type='S1', input_meta_data={"meta": "PDF file"}, owner=user)

        self.valid_payload = {
            "type": "PDF",
            "source_type": "S1",
            "input_meta_data": {"meta": "PDF file", "size": "1mb"},
            "owner": user.pk
        }

        self.invalid_payload = {
            "type": "PDF",
            "source_type": "S3",  # Invalid choice
            "input_meta_data": {"meta": "PDF file", "size": "1mb"},
            "owner": user.pk
        }
        client.login(username=self.username, password=self.password)

    def test_valid_update_document(self):
        response = client.put(
            reverse('doc-detail', kwargs={'pk': self.pdf_doc.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_document(self):
        response = client.put(
            reverse('doc-detail', kwargs={'pk': self.pdf_doc.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleDocumentTest(TestCase):
    """ Test module for deleting an existing document """
    username = "test"
    email = "test@xyz.com"
    password = "Test123!"
    client.login(username=username, password=password)

    def setUp(self):
        user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.pdf_doc = Document.objects.create(
            type='PDF', source_type='S1', input_meta_data={"meta": "PDF file"}, owner=user)
        client.login(username=self.username, password=self.password)

    def test_valid_delete_document(self):
        response = client.delete(reverse('doc-detail', kwargs={'pk': self.pdf_doc.pk})),
        self.assertEqual(response[0].status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_document(self):
        response = client.delete(
            reverse('doc-detail', kwargs={'pk': 30})),
        self.assertEqual(response[0].status_code, status.HTTP_404_NOT_FOUND)
