from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetDataView.as_view(), name='index'),
    path('user_task', views.create_csv, name='csv')
]
