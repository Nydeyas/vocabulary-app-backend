from django.contrib import admin
from .models import User, Category, Word

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Word)