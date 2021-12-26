from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    lat = models.DecimalField(decimal_places=4, max_digits=8)
    lng = models.DecimalField(decimal_places=4, max_digits=8)
    phone = models.CharField(max_length=50)
    website = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    catch_phrase = models.CharField(max_length=200)
    company_bs = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Todo(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField()

    def __str__(self):
        return self.title
