from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254,
                              blank=False,
                              verbose_name='Адрес электронной почты'
                              )

    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                verbose_name='Уникальный юзернейм'
                                )

    first_name = models.CharField(max_length=150,
                                  blank=False,
                                  verbose_name='Имя'
                                  )

    last_name = models.CharField(max_length=150,
                                 blank=False,
                                 verbose_name='Фамилия'
                                 )
    password = models.CharField(max_length=150,
                                blank=False,
                                verbose_name='Пароль')


class Subscriptions(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribe')
        ]