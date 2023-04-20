from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_year

SCORE_CHOICES = [(i, i) for i in range(1, 11)]
ROLE = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user'),
)


NAME_REGEX = RegexValidator(regex=r'^[\w.@+-]+$',
                            message='Некорректное имя',
                            code='invalid_username')


class User(AbstractUser):

    username = models.CharField('Никнейм', max_length=150, unique=True,
                                validators=[NAME_REGEX],)
    email = models.EmailField('Епочта', max_length=254, unique=True,)
    first_name = models.CharField('Имя пользователя',
                                  max_length=150, blank=True,)
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField('Роль пользователя', max_length=16,
                            choices=ROLE, default='user')
    confirmation_code = models.CharField('Код подтверждения',
                                         max_length=8,
                                         blank=True,)
    username = models.CharField('Никнейм', max_length=150, unique=True,)
    email = models.EmailField('Епочта', max_length=254, unique=True,)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150, blank=True,
    )
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        'Роль пользователя', max_length=16,
        choices=ROLE, default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=8,
        blank=True,
    )

    class Meta:
        unique_together = ('username', 'email')


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Жанр")
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Категория"
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Произведение')
    year = models.IntegerField(
        null=True,
        verbose_name="Год выпуска",
        validators=(validate_year, )
    )
    description = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles"
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year']


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(choices=SCORE_CHOICES)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=False
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_constraint'
            )
        ]
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
