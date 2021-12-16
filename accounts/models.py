from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.shortcuts import reverse


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, is_active=True, is_admin=False, password=None):
        if not username:
            raise ValueError("Must have a username")
        user = self.model(
            email=email,
            username=username,
            is_active=is_active,
            is_admin=is_admin
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, is_active=True, password=None):
        self.create_user(username, email, is_active, True, password)


class User(AbstractBaseUser):
    username = models.CharField(max_length=512, verbose_name="username")
    email = models.EmailField(verbose_name='email', max_length=512, unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def activate_email(self):
        self.email_confirmed = True
        self.is_active = True
        self.save()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])





