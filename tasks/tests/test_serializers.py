from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import exceptions
from rest_framework.serializers import DateTimeField

from tasks.models import Tasks
from tasks.serializers import TaskSerializer


class TaskSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="testuser", password="12345")
        Tasks.objects.create(title="Task 1", description="Description 1", done=False, author=user)

    def setUp(self):
        self.task = Tasks.objects.get(id=1)

    def test_deserialization(self):
        serialized_data = {
            "title": "Task",
            "description": "Description",
        }
        serializer = TaskSerializer(data=serialized_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, serialized_data)

    def test_invalid_serializer(self):
        serialized_data = {
            "description": "Description",
        }
        serializer = TaskSerializer(data=serialized_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(
            serializer.errors, {"title": [exceptions.ErrorDetail(string="This field is required.", code="required")]}
        )

    def test_contains_expected_fields(self):
        serializer = TaskSerializer(instance=self.task)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["id", "title", "description", "done", "created_at"]))

    def test_contains_expected_values(self):
        serializer = TaskSerializer(instance=self.task)
        data = serializer.data
        self.assertEqual(data["id"], self.task.id)
        self.assertEqual(data["title"], self.task.title)
        self.assertEqual(data["description"], self.task.description)
        self.assertEqual(data["done"], self.task.done)
        self.assertEqual(data["created_at"], DateTimeField().to_representation(self.task.created_at))

    def test_max_length_title(self):
        serialized_data = {
            "title": "Long title" * 250,
            "description": "Description",
        }

        serializer = TaskSerializer(data=serialized_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["title"][0].code, "max_length")
