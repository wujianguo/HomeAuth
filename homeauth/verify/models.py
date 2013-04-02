from django.db import models

# Create your models here.
from userena.utils import user_model_label
class VerifyUsers(models.Model):
    user = models.ForeignKey(user_model_label)
    pubkey = models.TextField(default = '')
