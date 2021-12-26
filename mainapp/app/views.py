from django.views.generic import TemplateView
from django.http import HttpResponse
import requests
import json
import csv
from django.shortcuts import render
from .models import User, Todo


class GetDataView(TemplateView):

    def get(self, request, **kwargs):

        users = self.get_data('users')
        for u in users:
            self.get_user(u)

        todos = self.get_data('todos')
        for t in todos:
            self.get_todo(t)

        return render(request, 'index.html', {'data': 'data fetched'})

    def get_user(self, user_data):
        user = User()
        user.id = user_data['id']
        user.name = user_data['name']
        user.username = user_data['username']
        user.email = user_data['email']
        user.street = user_data['address']['street']
        user.suite = user_data['address']['suite']
        user.city = user_data['address']['city']
        user.zipcode = user_data['address']['zipcode']
        user.lat = user_data['address']['geo']['lat']
        user.lng = user_data['address']['geo']['lng']
        user.phone = user_data['phone']
        user.website = user_data['website']
        user.company_name = user_data['company']['name']
        user.catch_phrase = user_data['company']['catchPhrase']
        user.company_bs = user_data['company']['bs']

        user.save()

    def get_todo(self, todo_data):
        todo = Todo()
        todo.id = todo_data['id']
        todo.userId = User.objects.get(id=todo_data['userId'])
        todo.title = todo_data['title']
        todo.completed = todo_data['completed']

        todo.save()

    def get_data(self, object):
        url = 'http://jsonplaceholder.typicode.com/' + object
        req = requests.get(url)
        r = json.loads(req.text)

        return r


def create_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="users_tasks.csv"'},)

    writer = csv.DictWriter(response, ['name', 'city', 'title', 'completed'])
    writer.writeheader()
    tasks = Todo.objects.all()

    for task in tasks:
        writer.writerow({'name': task.userId.name,
                         'city': task.userId.city,
                         'title': task.title,
                         'completed': task.completed})

    return response
