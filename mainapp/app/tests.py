from django.test import TestCase
from rest_framework.test import APIClient
import requests
import json
from .models import User, Todo
from .views import GetDataView


class ModelsTest(TestCase):
    def setUp(self):
        User.objects.create(id='123', name='Alan Ray', username='alanr',
                            email='ar@gmail.com', street='Oxford Street',
                            suite='23', city='Brighton', zipcode='123',
                            lat='50.2477', lng='12.3848', phone='23434535',
                            website='alanr.com', company_name='Google',
                            catch_phrase='lorem ipsum', company_bs='abcd')
        User.objects.create(id='2', name='Cindy Kane', username='cindyk',
                            email='ck@gmail.com', street='Brown Street',
                            suite='7', city='San Diego', zipcode='987',
                            lat='33.2477', lng='24.3848', phone='9898989',
                            website='cindyk.com', company_name='Apple',
                            catch_phrase='dolor emet', company_bs='wxyz')
        Todo.objects.create(id='1', userId=User.objects.get(id='123'),
                            title='First Todo', completed=True)
        Todo.objects.create(id='5', userId=User.objects.get(id='2'),
                            title='Second Todo', completed=False)

    def test_save_user_object(self):
        cindy = User.objects.get(name='Cindy Kane')
        alan = User.objects.get(name='Alan Ray')

        self.assertEqual(cindy.city, 'San Diego')
        self.assertEqual(alan.company_name, 'Google')
        self.assertNotEqual(alan.city, 'San Diego')

    def test_save_todo_object(self):
        first = Todo.objects.get(title='First Todo')
        second = Todo.objects.get(title='Second Todo')

        self.assertEqual(first.userId, User.objects.get(id='123'))
        self.assertEqual(second.completed, False)
        self.assertNotEqual(second.userId, '123')


class GetDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        users = GetDataView.get_data(GetDataView(), 'users')
        for u in users:
            GetDataView.get_user(GetDataView(), u)

        todos = GetDataView.get_data(GetDataView(), 'todos')
        for t in todos:
            GetDataView.get_todo(GetDataView(), t)

    def test_response_ok(self):
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)

    def test_response_invalid(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_user_in_db(self):
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(name='Ervin Howell')

        self.assertEqual(user1.name, 'Leanne Graham')
        self.assertEqual(user2.city, 'Wisokyburgh')
        self.assertNotEqual(user2.id, 4)

    def test_todo_in_db(self):
        todo1 = Todo.objects.get(id=1)
        todo2 = Todo.objects.get(id=15)

        self.assertEqual(todo1.title, 'delectus aut autem')
        self.assertEqual(todo2.completed, True)
        self.assertNotEqual(todo1.completed, True)

    def test_user_db_records(self):
        users_url = 'http://jsonplaceholder.typicode.com/users'
        req = requests.get(users_url)
        r = json.loads(req.text)

        self.assertEqual(User.objects.all().count(), len(r))

    def test_todo_db_records(self):
        todos_url = 'http://jsonplaceholder.typicode.com/todos'
        req = requests.get(todos_url)
        r = json.loads(req.text)

        self.assertEqual(Todo.objects.all().count(), len(r))


class GetCSVViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_response_ok(self):
        response = self.client.get('/app/user_task')
        self.assertEqual(response.status_code, 200)

    def test_response_invalid(self):
        response = self.client.get('/user_task')
        self.assertEqual(response.status_code, 404)
