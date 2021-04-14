from django.conf import settings
from django.db import models


class Phone(models.Model):
    phone = models.CharField(max_length=13)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # noqa E501

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'telefone'
        verbose_name_plural = 'telefones'

    def __str__(self):
        return self.user.email
