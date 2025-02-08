from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from materials.models import Lesson, Course
from users.models import User, Subscribe


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@sky.pro", username="admin")
        self.course = Course.objects.create(name="Course_1")
        self.lesson = Lesson.objects.create(name="Lesson_1", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {"name": "test",
                "course": 1,
                "owner": 1}

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"name": "test_update"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get("name"), "test_update"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")

        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'name': self.lesson.name, 'description': None,
             'image': None, 'video_url': None, 'course': self.course.pk, 'owner': self.user.pk}]}

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data, result
        )


class SubscribeTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@sky.pro", username="admin")
        self.course = Course.objects.create(name="Course_1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_course(self):
        url = reverse("users:subscribe")
        data = {"course": self.user.pk,
                "user": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")

        subscription = Subscribe.objects.filter(user=self.user, course=self.course)
        self.assertTrue(subscription.exists())

    def test_unsubscribe_from_course(self):
        url = reverse("users:subscribe")
        Subscribe.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, {"course": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")

        subscription = Subscribe.objects.filter(user=self.user, course=self.course)
        self.assertFalse(subscription.exists())

