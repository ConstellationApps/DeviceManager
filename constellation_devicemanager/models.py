from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    MAC = models.CharField(primary_key=True, max_length=17)
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner) + ": " + self.name
