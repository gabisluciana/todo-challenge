from django.test import TestCase
from django.contrib.auth.models import User

from tasks.models import Tasks


class TasksTest(TestCase):
    """Test module for Tasks model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username="testuser", password="12345")
        Tasks.objects.create(title="Task 1", description="Task 1 description", author=user)
        Tasks.objects.create(title="Task 2", done=True, author=user)
        Tasks.objects.create(title="T" * 400, description="Description 3", done=False, author=user)

    def test_default_done_value(self):
        task = Tasks.objects.get(id=1)
        self.assertFalse(task.done)

    def test_inserted_done_value(self):
        task = Tasks.objects.get(id=2)
        self.assertTrue(task.done)

    def test_optional_description_value(self):
        task = Tasks.objects.get(id=2)
        self.assertIsNone(task.description)

    def test_str_method(self):
        task = Tasks.objects.get(id=1)
        expected_str = f"{task.title} - By: {task.author.username}"
        self.assertEquals(str(task), expected_str)
