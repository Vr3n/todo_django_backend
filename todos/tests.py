from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone

from todos.models import Todo

# Create your tests here.

todo_test_data = {
    'title': 'Test Data',
    'description': "This is a test data",
    'start_date': timezone.now(),
}

class TodoModelTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username="vr3n", email="vr3n@gmail.com")
        self.user.set_password('Django@123')
        self.user.save()

        self.c = Client()
        self.c_user = self.c.login(username=self.user.username, password="Django@123")

        self.todo = None


    def test_create_todo(self):
        pre_count = Todo.objects.all().count()
        self.todo = Todo.objects.create(user=self.user, **todo_test_data)
        post_count = Todo.objects.all().count()

        self.assertGreater(post_count, pre_count)


    def test_read_todo(self):
        todo_obj = Todo.objects.get(title=todo_test_data['title'])

        self.assertEqual(todo_obj.title, todo_test_data['title'])
        self.assertEqual(todo_obj.description, todo_test_data['description'])
        self.assertEqual(todo_obj.start_date, todo_test_data['start_date'])
