from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.

class Rules(models.Model):
    rule = JSONField()
