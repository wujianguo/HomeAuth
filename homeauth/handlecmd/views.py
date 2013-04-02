# Create your views here.
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from userena.decorators import secure_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from handlecmd.forms import CmdForm,VerifyForm
from handlecmd.models import RemoteCmd
from userena.utils import user_model_label
import json,logging
#logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')
@secure_required
@login_required
@csrf_protect
def recvcmdFromWeb(request):
    user = request.user
    c = {}
    c.update(csrf(request))
    try:
        p = RemoteCmd.objects.get(user=user)
    except RemoteCmd.DoesNotExist:
        p = RemoteCmd(user = user)
        p.save()
    if request.method == 'POST':
        form = CmdForm(request.POST)
        if form.is_valid():
            p.camera_cmd = form.cleaned_data['camera_cmd']
            p.screen_cmd = form.cleaned_data['screen_cmd']
            p.audio_out_cmd = form.cleaned_data['audio_out_cmd']
            p.last_recvcmd_time = timezone.now()
            p.new_cmd = True
            p.save()
            c.update({'ok':True})
        else:
            logging.error('invalid data')
    else:
        logging.error('method must post')
    c.update({'remotecmd':p})
    return render_to_response('handlecmd/remotecmd.html',c)
def recvcmdFromApp(request):
    pass
def getcmd(request):
    rescmd = {'camera_cmd':'','screen_cmd':'','audio_out_cmd':'','new':False}
    resmsg = {'err':'ok','response':rescmd}
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            user = form.getUser()
            if user:
                try:
                    p = RemoteCmd.objects.get(user=user)
                except RemoteCmd.DoesNotExist:
                    resmsg['err'] = 'invalid user'
                else:
                    rescmd.update({'camera_cmd':p.camera_cmd,'screen_cmd':p.screen_cmd,'audio_out_cmd':p.audio_out_cmd,'new':p.new_cmd})
                    resmsg['response'] = rescmd
                    p.last_getcmd_time = timezone.now()
                    p.new_cmd = False
                    p.save()
            else:
                resmsg['err'] = 'invalid user'
        else:
            resmsg['err'] = 'invalid post data'
    else:
        resmsg['err'] = 'method must post'
    return HttpResponse(json.dumps(resmsg), content_type="application/json")