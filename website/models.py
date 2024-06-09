from django.db import models


class User(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    username = models.CharField(db_column='username', max_length=50)
    email = models.EmailField(db_column='email', max_length=80)
    password = models.CharField(db_column='password', max_length=255)

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return f"{self.username} ({self.email})"


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
