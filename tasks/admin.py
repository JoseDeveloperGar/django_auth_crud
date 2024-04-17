from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    """
    Este fragmento de codigo sirve para indicarle a django que el campo "created" solo se puede ver mas no editar 
    """

# Register your models here.
admin.site.register(Task, TaskAdmin)