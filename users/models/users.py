from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username=models.CharField(
        unique=True,
        max_length=20
    )
    first_name=models.CharField(
        max_length=20,
    )
    last_name=models.CharField(
        max_length=20
    )
    email=models.EmailField(
        unique=True,
    )
    auth_token=models.CharField(
        max_length=500,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
    
    

