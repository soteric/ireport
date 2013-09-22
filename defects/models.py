from django.db import models

# Create your models here.
class Defects(models.Model):
    type = models.CharField(max_length=200)
    number = models.IntegerField()

    def __unicode__(self):
        return self.type