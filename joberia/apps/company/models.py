from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    image = models.ImageField()
    address = models.TextField()

    def __str__(self):
        return self.name
