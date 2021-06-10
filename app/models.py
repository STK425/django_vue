from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    type = models.CharField(max_length=32)

    def __unicode__(self):
        return (self.user_name, self.password, self.phone, self.type)
