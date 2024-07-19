from django.db import models

class City(models.Model):

    name=models.CharField(max_length=255 , verbose_name="Город")

    def __str__(self) -> str:
        return self.name


