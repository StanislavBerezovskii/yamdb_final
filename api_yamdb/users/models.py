from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from .validators import validate_username

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin'),
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        unique=True,
        validators=[validate_username, ],
    )
    email = models.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        # Дефолтное значение 150 равно значению из ТЗ, но на всякий случай
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        # Дефолтное значение 150 равно значению из ТЗ, но на всякий случай
        max_length=150,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=settings.MAX_ROLE_LENGTH,
        choices=ROLES,
        default=USER,
    )

    @property
    def is_admin_or_superuser(self):
        return self.role == ADMIN or self.is_staff or self.is_superuser

    # Стас, Иван, это вам на всякий случай — вдруг пригодится)
    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
