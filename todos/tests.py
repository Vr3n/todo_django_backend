from django.contrib.auth import get_user_model
from rest_framework import status
from django.test import Client, TestCase
from rest_framework.test import APITestCase
from django.utils import timezone
import datetime
from django.urls import reverse

from todos.models import Todo

# Create your tests here.

todo_test_data = {
    "title": "Test Data",
    "description": "This is a test data",
    "start_date": timezone.now(),
}


class TodoModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="vr3n", email="vr3n@gmail.com"
        )
        self.user.set_password("Django@123")
        self.user.save()

        self.c = Client()
        self.c_user = self.c.login(
            username=self.user.username,
            password="Django@123"
        )

        self.todo = None

    def test_create_todo(self):
        pre_count = Todo.objects.all().count()
        self.todo = Todo.objects.create(user=self.user, **todo_test_data)
        post_count = Todo.objects.all().count()

        self.assertGreater(post_count, pre_count)


class TodoAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username='virus', email="vr3n@gmail.com")

        self.user.set_password('Django@123')

        self.user.save()

        self.c = Client()
        self.c.force_login(self.user)

        self.valid_todo_data = {
            'title': "Test Todo",
            'description': "Testing in test.",
            'start_date': datetime.date.today(),
        }

        self.invalid_todo_data = {
            'start_date': datetime.date.today(),
        }

    def test_create_todo_api(self):

        res = self.c.post(reverse('todo-list'), data=self.valid_todo_data)

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def test_create_todo_api_fail(self):

        res = self.c.post(reverse('todo-list'), data=self.invalid_todo_data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'title': ['This field is required.']}, res.json())

    def test_update_todo_api(self):

        res = self.c.post(reverse('todo-list'), data=self.valid_todo_data)

        data = res.json()

        todo_obj = Todo.objects.get(title=data['title'])

        self.valid_todo_data['title'] = 'updated_title'
        self.valid_todo_data['description'] = 'updated_description'
        print(self.valid_todo_data)

        update_res = self.c.put(
            reverse('todo-detail', kwargs={'pk': todo_obj.id}),
            data=self.valid_todo_data,
            content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, update_res.status_code)
        self.assertNotEqual(data['title'], self.valid_todo_data['title'])
