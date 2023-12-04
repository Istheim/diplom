import random
import string
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    phone = models.CharField(_('phone number'), max_length=12, **NULLABLE)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    is_verified = models.BooleanField(_('verified'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('username', 'phone')


#    # Создание 6-ти значного ивайт-кода и сохранение его в бд
#    def save(self, *args, **kwargs):
#        if not self.invitation_code:
#            all_symbols = list(string.ascii_lowercase + string.digits)
#            code_items = []
#
#            for i in range(6):
#                cod = random.choice(all_symbols)
#                code_items.append(cod)
#
#            result = ''.join(str(item) for item in code_items)
#            self.invitation_code = result
#        super().save(*args, **kwargs)
#
#
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
