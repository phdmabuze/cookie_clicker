from django.contrib import admin
from upgrades.models import Upgrade, UserUpgrade


class UpgradeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Upgrade, UpgradeAdmin)


class UserUpgradeAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserUpgrade, UserUpgradeAdmin)