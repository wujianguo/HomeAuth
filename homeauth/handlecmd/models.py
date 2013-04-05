from django.db import models

# Create your models here.
from django.utils import timezone
from userena.utils import user_model_label
class RemoteCmd(models.Model):
    user = models.ForeignKey(user_model_label)
    cmdline = models.CharField(max_length = 160,default = '')
    client_state = models.TextField(default = '')
    help_msg = models.TextField(default = 'help msg')
    new_cmd = models.BooleanField(default = False)
    last_recvcmd_time = models.DateTimeField(default = timezone.now())
    last_getcmd_time = models.DateTimeField(default = timezone.now())
