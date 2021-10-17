from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    email = models.EmailField(max_length=254,
                              blank=False,
                              verbose_name='Адрес электронной почты'
                              )

    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                verbose_name='Уникальный юзернейм',
                                validators=[RegexValidator(
                                    regex=r'^[\w.@+-]+\Z',
                                    message='Вы ввели недопустимые символы')
                                ]
                                )

    first_name = models.CharField(max_length=150,
                                  blank=False,
                                  verbose_name='Имя'
                                  )

    last_name = models.CharField(max_length=150,
                                 blank=False,
                                 verbose_name='Фамилия'
                                 )



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
                                    name='unique_subscribe'),
            models.CheckConstraint(
                check=~models.Q(user_id=models.F('author_id')),
                name="follower_is_not_following",
            ),

        ]