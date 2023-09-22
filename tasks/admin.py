from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    # Indicando que campos se veran como solo lectura en el admin
    readonly_fields = ("created",)


# Register your models here.
admin.site.register(Task, TaskAdmin)
