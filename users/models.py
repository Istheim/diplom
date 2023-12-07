from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from users.utils import generate_digit_code

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, username=None, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')

        # Если username не предоставлен, используем phone
        if not username:
            username = phone

        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_superuser(phone, password, username, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=30, verbose_name='Имя пользователя', unique=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True)
    referral_code = models.CharField(max_length=6, null=True, default=None)
    else_referral_code = models.OneToOneField('self', on_delete=models.DO_NOTHING, null=True, default=None)
    is_verified = models.BooleanField(('verified'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self) -> str:
        return str(self.phone)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Code(models.Model):
    code = models.CharField(max_length=4, default=generate_digit_code)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.code)
