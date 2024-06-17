from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializer import *


def home(request):
    return render(request, 'home.html', {})


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # # Filtering
        # name = self.request.query_params.get('name')
        # if name:
        #     queryset = queryset.filter(username=name)
        return queryset


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class WordView(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
