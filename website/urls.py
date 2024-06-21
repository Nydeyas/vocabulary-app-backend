from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/register', RegisterView.as_view()),
    path('api/user', UserView.as_view()),
    path('api/category', CategoryView.as_view()),
    path('api/word', WordView.as_view()),
    path('api/user/<int:user_id>', UserDetailApiView.as_view()),
    path('api/category/<int:category_id>', CategoryDetailApiView.as_view()),
    path('api/word/<int:word_id>', WordDetailApiView.as_view()),
]
