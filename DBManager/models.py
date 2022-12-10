from django.db import models


class Database(models.Model):
    name = models.CharField(max_length=30)


class Table(models.Model):
    name = models.CharField(max_length=30)
    data = models.JSONField(default=dict, blank=True)
    database = models.ForeignKey('Database', on_delete=models.CASCADE)






