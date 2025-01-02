from django.contrib import admin
from django.contrib.auth.models import Group

from . import models

# Register your models here.
admin.site.register(models.Week)
admin.site.register(models.SchoolClass)
admin.site.register(models.Score)
admin.site.unregister(Group)