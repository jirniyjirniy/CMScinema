from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class CustomUser(models.Model):
    class Languages(models.TextChoices):
        ENGLISH = 'EN', "English"
        UKRAINE = 'UA', 'Ukraine'

    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    second_name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=10, choices=Languages.choices, default=Languages.UKRAINE)
    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.MALE)
    card = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
