from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('<slug:slug>/', views.project_detail, name='detail'),
]
