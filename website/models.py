from django.contrib.auth.models import (
    PermissionsMixin, BaseUserManager, AbstractBaseUser, UserManager
)
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    is_active = True
    is_anonymous = False
    is_authenticated = True

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Category(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=100)
    word_language = models.CharField(db_column='word_language', max_length=30, null=True, blank=True)
    translation_language = models.CharField(db_column='translation_language', max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
        return f"{self.name}"


class Word(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    word = models.CharField(db_column='word', max_length=255, null=True, blank=True)
    translation = models.CharField(db_column='translation', max_length=255, null=True, blank=True)
    is_learned = models.BooleanField(db_column='is_learned', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'word'

    def __str__(self):
        return f"{self.word} - {self.translation}"
