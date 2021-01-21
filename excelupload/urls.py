from django.urls import path

from . import views

urlpatterns = [
    path('', views.InsertData.as_view()),
    path('get', views.GetData.as_view()),
    path('delete', views.DeleteData.as_view()),
]
