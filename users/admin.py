from django.contrib import admin

from users.models import User, Code

admin.site.register(Code)
admin.site.register(User)
