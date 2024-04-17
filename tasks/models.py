from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    datecompleted = models.DateTimeField(null=True, blank=True) 
    """
    'blank' se refiere a la validación de formularios y controla si un campo puede estar vacío en los formularios HTML, mientras que 'null' se refiere a la base de datos y controla si un campo puede contener valores nulos en la base de datos.
    """
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' by ' + self.user.username + ' (' + str(self.user.id)  + ')'
    
    
