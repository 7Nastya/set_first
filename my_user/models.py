from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Создает и сохраняет пользователя с введенным им email и паролем.
        """
        if not username:
            raise ValueError('email должен быть указан')
        # email = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=64, verbose_name="Ник", unique=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    date_joined = models.DateTimeField(null=True, blank=True, verbose_name="Дата присоединения")
    email = models.EmailField(max_length=128, verbose_name="Адрес элктронной почты")
    first_name = models.CharField(max_length=256, verbose_name="Имя")
    last_name = models.CharField(max_length=256, verbose_name="Фамилия")

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователя'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
