from django.db import models

# Create your models here.
from django.utils import timezone
from userena.utils import user_model_label
class RemoteCmd(models.Model):
    user = models.ForeignKey(user_model_label)
    camera_cmd = models.CharField(max_length = 80,default = '')
    screen_cmd = models.CharField(max_length = 80,default = '')
    audio_out_cmd  = models.CharField(max_length = 80,default = '')
    new_cmd = models.BooleanField(default=False)
    last_recvcmd_time = models.DateTimeField(default = timezone.now())
    last_getcmd_time = models.DateTimeField(default = timezone.now())