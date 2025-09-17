import math

from django.db import models

import utils


class TgUser(models.Model):
    tg_id = models.BigIntegerField(unique=True, primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)

    balance = models.BigIntegerField(default=0)
    income_per_second = models.IntegerField(default=1)
    balance_last_updated_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ["-created_at"]
        db_table = "tg_user"

    def __str__(self):
        return self.username or f"Player#{self.tg_id}"

    def get_balance_with_income(self):
        return math.floor(
            self.balance + self.income_per_second * (utils.get_time() - self.balance_last_updated_at).total_seconds())

    def get_username(self):
        return self.username or f"Player#{self.tg_id}"
