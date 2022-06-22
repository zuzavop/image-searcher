from django.db import models


class Image(models.Model):
    index = models.IntegerField(default=0)
    classes = models.TextField()

    def __str__(self):
        return self.index