import logging
from datetime import date, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, override_settings
from rest_framework_simplejwt.tokens import AccessToken

from tasks.models import Tasks


logging.disable(logging.CRITICAL)


class BaseTasksApiTestCase(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user1", password="123")

        self.tasks = [
            Tasks.objects.create(title=f"Task {i}", description=f"Description {i}", author=self.user)
            for i in range(1, 4)
        ]

        user2 = User.objects.create_user(username="user2", password="123")
        self.other_tasks = [
            Tasks.objects.create(title=f"Other Task {i}", description=f"Other Description {i}", author=user2)
            for i in range(1, 2)
        ]

        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))

        return super().setUp()


class TaskListApiTest(BaseTasksApiTestCase):

    def test_list_own_tasks(self):
        response = self.client.get(reverse("tasks-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.tasks))

    def test_filter_own_tasks_content(self):
        response = self.client.get(reverse("tasks-list"), QUERY_STRING="content=Task 1")
        content_tasks = list(filter(lambda t: "Task 1" in t.title or "Task 1" in t.description, self.tasks))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(content_tasks))

    def test_filter_own_tasks_date(self):
        today = date.today()
        response = self.client.get(reverse("tasks-list"), QUERY_STRING=f'date={today.strftime("%Y-%m-%d")}')
        date_tasks = list(filter(lambda t: t.created_at.date() == today, self.tasks))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(date_tasks))

    def test_filter_own_tasks_content_date(self):
        today = date.today()
        response = self.client.get(
            reverse("tasks-list"), QUERY_STRING=f'content=Task 1&date={today.strftime("%Y-%m-%d")}'
        )
        content_today_tasks = list(
            filter(
                lambda t: t.created_at.date() == today and ("Task 1" in t.title or "Task 1" in t.description),
                self.tasks,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(content_today_tasks))


class TaskCreateApiTest(BaseTasksApiTestCase):
    def test_create_task(self):
        payload = {"title": "test task", "description": "test description"}
        response = self.client.post(reverse("tasks-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tasks.objects.filter(title="test task", author=self.user).exists())


class TaskGetDetailApiTest(BaseTasksApiTestCase):
    def test_get_task(self):
        response = self.client.get(reverse("tasks-detail", kwargs={"pk": self.tasks[0].pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.tasks[0].title)

    def test_get_other_user_task(self):
        response = self.client.get(reverse("tasks-detail", kwargs={"pk": self.other_tasks[0].pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"].code, "not_found")


class TaskUpdateApiTest(BaseTasksApiTestCase):

    def test_update_own_task(self):
        payload = {"title": "updated test task", "description": "updated test description"}
        response = self.client.put(reverse("tasks-detail", kwargs={"pk": self.tasks[0].pk}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Tasks.objects.filter(title="updated test task", author=self.user).exists())

    def test_update_other_user_task(self):
        payload = {"title": "updated test task", "description": "updated test description"}
        response = self.client.put(reverse("tasks-detail", kwargs={"pk": self.other_tasks[0].pk}), payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Tasks.objects.filter(title="updated test task", author=self.user).exists())


class TaskDeleteApiTest(BaseTasksApiTestCase):

    def test_delete_own_task(self):
        response = self.client.delete(reverse("tasks-detail", kwargs={"pk": self.tasks[0].pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tasks.objects.filter(pk=self.tasks[0].pk).exists())

    def test_delete_other_user_task(self):
        response = self.client.delete(reverse("tasks-detail", kwargs={"pk": self.other_tasks[0].pk}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Tasks.objects.filter(pk=self.other_tasks[0].pk).exists())


class TaskCompleteApiTest(BaseTasksApiTestCase):

    def test_complete_own_task(self):
        response = self.client.patch(reverse("tasks-done", kwargs={"pk": self.tasks[0].pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Tasks.objects.filter(pk=self.tasks[0].pk, done=True).exists())

    def test_complete_other_user_task(self):
        response = self.client.patch(reverse("tasks-done", kwargs={"pk": self.other_tasks[0].pk}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Tasks.objects.filter(pk=self.other_tasks[0].pk, done=True).exists())
