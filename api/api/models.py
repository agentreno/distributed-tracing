from django.db import models


class Event(models.Model):
    data = models.JSONField()


class Vulnerability(models.Model):
    data = models.JSONField()
