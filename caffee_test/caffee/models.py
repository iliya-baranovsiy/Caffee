from django.db import models


# Create your models here.

class Caffe(models.Model):
    table_number = models.IntegerField()
    items = models.JSONField()
    total_price = models.DecimalField(decimal_places=10,max_digits=10)
    status = models.CharField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        return self.status
