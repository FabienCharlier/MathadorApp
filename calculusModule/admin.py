from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Week)
admin.site.register(models.SchoolClass)
admin.site.register(models.Score)