from django.db import models


class Upgrade(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    income_increase = models.IntegerField()
    photo = models.ImageField(upload_to="upgrades/", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Upgrade"
        verbose_name_plural = "Upgrades"
        db_table = "upgrade"

    def __str__(self):
        return self.name


class UserUpgrade(models.Model):
    user = models.ForeignKey(
        "users.TgUser",
        on_delete=models.CASCADE,
        related_name="user_upgrades"
    )
    upgrade = models.ForeignKey(
        Upgrade,
        on_delete=models.CASCADE,
        related_name="purchased_by"
    )
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "upgrade")
        verbose_name = "User Upgrade"
        verbose_name_plural = "User Upgrades"
        db_table = "user_upgrade"

    def __str__(self):
        return f"{self.user} -> {self.upgrade}"