from django.urls import path
from . import views

app_name = "ml_deploy"
urlpatterns = [
    path('', views.IrisHome.as_view(), name='iris_home'),
    path('predict/', views.irisPredict, name='iris_predict'),
]