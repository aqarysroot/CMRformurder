from django.contrib import admin
from .models import Order, Target, Payment
# Register your models here.
admin.site.register(Order)
admin.site.register(Target)
admin.site.register(Payment)
