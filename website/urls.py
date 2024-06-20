from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view()),
    path('api/user', UserView.as_view(), name="API - user"),
    path('api/category', CategoryView.as_view(), name="API - category"),
    path('api/word', WordView.as_view(), name="API - word"),
]
