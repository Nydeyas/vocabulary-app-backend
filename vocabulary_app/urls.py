"""
URL configuration for vocabulary_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.views.generic.base import RedirectView
from website.views import *

urlpatterns = [
    path('api', HomeView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/register', RegisterView.as_view()),
    path('api/user', UserView.as_view()),
    path('api/category', CategoryView.as_view()),
    path('api/word', WordView.as_view()),
    path('api/user/<int:user_id>', UserDetailApiView.as_view()),
    path('api/category/<int:category_id>', CategoryDetailApiView.as_view()),
    path('api/word/<int:word_id>', WordDetailApiView.as_view()),

    # Redirect to HomeView
    path('', RedirectView.as_view(url='/api'), name='api-redirect'),
    # Redirect uppercase URLs to lowercase
    path('<str:slug>/', RedirectView.as_view(url='/<slug_lowercase>/')),
]
