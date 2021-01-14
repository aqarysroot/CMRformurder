from django.utils.translation import gettext_lazy as _
from django.db import models

class Status(models.TextChoices):
    COMPLETED = 'CMPD', _('COMPLETED')
    WAITING = 'WTNG', _('WAITING')
    CANCELED = 'CNLD', _('CANCELED')

class LifeStatus(models.TextChoices):
    DEAD = 'DEAD', _('DEAD')
    ALIVE = 'ALV', _('ALIVE')


