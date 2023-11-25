# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True, verbose_name=_('groups'))
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.username
