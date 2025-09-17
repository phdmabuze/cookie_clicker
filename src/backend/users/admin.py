from django.contrib import admin

from users.models import TgUser


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TgUser, UserAdmin)
