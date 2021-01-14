from django.db import models
from users.models import User
from datetime import datetime
 
from . import defines as D

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    status = models.CharField(max_length=4, choices=D.Status.choices, default=D.Status.WAITING)

class Target(models.Model):
    username = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    age = models.IntegerField()
    time_to_death = models.DateTimeField(auto_now=False)
    status = models.CharField(max_length=4, choices=D.LifeStatus.choices, default=D.LifeStatus.ALIVE)

    def save(self, *args, **kwargs):
        if self.time_to_death >= datetime.now():
            self.status = D.LifeStatus.DEAD
        super(Target, self).save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user',null=True)
    purchased = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    


