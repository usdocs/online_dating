from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

SEX = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='images/',
        verbose_name='Аватарка'
    )

    sex = models.CharField(
        'Пол',
        max_length=7,
        choices=SEX,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой почтой существует.',
        },
    )

    username = models.CharField(
        'Никнейм',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator],
        error_messages={
            'unique': 'Пользователь с таким именем существует.',
        },
    )

    password = models.CharField(
        'Пароль',
        max_length=150,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username


class Match(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liker',
        verbose_name='Лайкер'
    )
    liking = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liking',
        verbose_name='Объект симпатии'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'liking'],
                name='unique_together'
            )
        ]
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} {self.liking}'
