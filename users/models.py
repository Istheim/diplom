import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=30, verbose_name='Имя пользователя', unique=True)
    password = models.CharField(max_length=128, verbose_name='Пароль')
    number_phone = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True)
    invitation_code = models.CharField(max_length=6, null=True, default=None)
    is_invitation_code_used = models.BooleanField(default=False)
    else_invitation_code = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, default=None)
    activated_else_invitation_code = models.CharField(max_length=6, null=True, default=None)

    # Создание 6-ти значного ивайт-кода и сохранение его в бд
    def save(self, *args, **kwargs):
        if not self.invitation_code:
            all_symbols = list(string.ascii_lowercase + string.digits)
            code_items = []

            for i in range(6):
                cod = random.choice(all_symbols)
                code_items.append(cod)

            result = ''.join(str(item) for item in code_items)
            self.invitation_code = result
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Code(models.Model):
    code = models.CharField(max_length=4, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.code)

    # Создание 4-рех значного кода аунтификации и сохранение его в бд
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(4):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.code = code_string
        super().save(*args, **kwargs)
