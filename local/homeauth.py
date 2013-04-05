#! /usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__config__  = 'homeauth.ini'
import requests,os.path,urllib,logging,time,subprocess
import json,threading,ConfigParser,getopt
from Crypto.PublicKey import RSA
import Crypto.Random
ROOT_DIR = os.path.dirname(__file__)
class Common(object):
    """Global Config Object"""
    def __init__(self):
        """load config from proxy.ini"""
#        ConfigParser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
        self.CONFIG = ConfigParser.ConfigParser()
        self.CONFIG.read(os.path.join(os.path.dirname(__file__), __config__))
        self.PROXY_VISIBLE        = self.CONFIG.getint('proxy', 'visible')
        self.PROXY                = {'http':self.CONFIG.get('proxy', 'http')} if self.PROXY_VISIBLE else None
        self.PROXY_USER           = self.CONFIG.get('proxy','username')
        self.PROXY_PASSWORD       = self.CONFIG.get('proxy','password')
        if self.PROXY_PASSWORD:
            self.PROXY_PASSWORD = int(self.PROXY_PASSWORD)
        
        self.SERVER_PUBKEY_URL    = self.CONFIG.get('serveurls','id_rsa_pub')
        self.SERVER_CMD_URL       = self.CONFIG.get('serveurls','get_cmd_url')
       
        self.PRIVKEY_PATH         = self.CONFIG.get('user','privkey_path')
        self.USER_EMAIL           = self.CONFIG.get('user','email')
        self.LOG_LEVEL            = self.CONFIG.get('log','loglevel')
        self.REQUESTS_TIME        = self.CONFIG.getint('requests','time')

    def info(self):
        info = ''
        info += '------------------------------------------------------\n'
        info += 'homeauth version : %s\n'%__version__
        if self.PROXY_VISIBLE:
            info += 'proxy : %s\n'%self.PROXY
        info += 'pubkey url : %s\n'%self.SERVER_PUBKEY_URL
        info += 'cmd url    : %s\n'%self.SERVER_CMD_URL
        info += 'privkey path: %s\n'%self.PRIVKEY_PATH
        info += 'user email: %s\n'%self.USER_EMAIL
        info += 'requests time:%d\n'%self.REQUESTS_TIME
        info += 'log level  : %s\n'%self.LOG_LEVEL
        info += '------------------------------------------------------\n'
        return info

common = Common()
print(common.info())
class DoubanFM():
    def __init__(self):
        self.logined = False
        self.history = []
        self.song_list = []
        self.channel = 1
        self.cur_song = {'sid':''}
    def login(self,email,passwd):
        payload={'email':email,'password':passwd,'app_name':'radio_desktop_win','version':100}
        url = 'http://www.douban.com/j/app/login'
        r = requests.post(url, data=payload,proxies=common.PROXY)
        data = r.json()
        if data['err']!='ok':
            logging.error('login failed')
            return False
        self.user_id = data['user_id']
        self.expire = data['expire']
        self.token = data['token']
        self.logined = True
        return True
    def changeChannel(self,channel):
        self.channel = channel
    def playSong(self):
        if len(self.song_list) < 2:
            self.song_list.extend(self.getSongList(self.channel))
        song = self.song_list.pop(0)
        self.history.append(song)
        if len(self.history) > 15:
            self.history.pop(0)
        self.cur_song = song
        logging.debug('%s %s'%(song['artist'],song['title']))
        return song
    def getParams(self,channel):
        type = 'n'
        h = ''
        if len(self.history)>0:
            type = 'p'
            h = '|'+':p|'.join([x['sid'] for x in self.history])+':p'
            self.history = []
        if self.logined:
            params = {'app_name':'radio_desktop_win','version':100,'user_id':self.user_id,
                'expire':self.expire,'token':self.token,'type':type,'sid':self.cur_song['sid'],'h':h,'channel':channel}
        else:
            params = {'app_name':'radio_desktop_win','version':100,'type':type,'sid':self.cur_song['sid'],'h':h,'channel':channel}
        return params
    def getSongList(self,channel):
        url = 'http://www.douban.com/j/app/radio/people'
        payload = self.getParams(channel)
        r = requests.get(url,params=payload,proxies=common.PROXY)
        return r.json()['song']
    def getChannels(self):
        url = 'http://www.douban.com/j/app/radio/channels'
        r = requests.get(url,proxies=common.PROXY)
        return r.json()['channels']
    def printChannels(self):
        self.channels = ''
        if not self.channels:
            self.channels = self.getChannels()
        for channel in self.channels:
            logging.info('%d\t%s\t%s'%(channel['channel_id'],channel['name'],channel['name_en']))
class MusicPlayer(threading.Thread):
    def __init__(self,songnum,email='',passwd=''):
        super(MusicPlayer, self).__init__()
        self.doubanFM = DoubanFM()
        self.cancelplay = False
        try:
            self.songnum = int(songnum)
        except Exception,data:
            logging.error(data)
            self.songnum = 1
        self.pro = None
        if email and passwd:
            if self.doubanFM.login(email,passwd):
                self.doubanFM.changeChannel(0)
    def run(self):
        self.playSongs(self.songnum)
    def playSongs(self,songnum):
        if songnum < 0:
            return
        playalways = False
        if songnum == 0:
            playalways = True
        while True:
            song = self.doubanFM.playSong()
            self.playing(song['url'])
            songnum = songnum - 1
            if (not playalways and songnum == 0) or self.cancelplay:
                break
        self.cancelplay = False
    def playing(self,url):
        cmd = ['ffplay',url,'-nodisp','-autoexit']
        self.pro = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            self.pro.communicate()
        except Exception,data:
            logging.error(data)
            if self.pro.returncode is None:
                self.pro.terminate()
    def cancelplaying(self):
        self.cancelplay = True
        if self.pro and self.pro.returncode is None:
            self.pro.terminate()
class myDropbox():
    def __init__(self):
        pass
    def createFolder(self,path):
        pass
    def uploadFile(self,upfile,tofile):
        pass
filehandle = myDropbox()
class CameraCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        logging.debug(cmd)
    def terminate(self):
        pass
class ScreenCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        logging.debug(cmd)
        return
        cmd = cmd.lower()
        if len(cmd)<=1 or cmd[0] != 't':
            logging.error('old cmd')
            return
        if cmd[1] == 't':
            if len(cmd)<=2:
                return
            if cmd[2] == 'u':
                p = self.takeAshot()
                filehandle.uploadFile(p,'')
    def takeAShot(self):
        return ''
    def terminate(self):
        pass
class AudioCmd():
    def __init__(self):
        self.music_player = None
    def runCmd(self,cmd):
        logging.debug(cmd)       
        optlist,args = getopt.getopt(cmd,'p:s')
        for o,v in optlist:
            if o == '-p':
                if self.music_player is None or not self.music_player.isAlive():
                    try:
                        self.music_player = MusicPlayer(v)
                        self.music_player.start()
                    except Exception,data:
                        logging.error(data)
            if o == '-s':
                self.terminate()
    def terminate(self):
        if self.music_player is not None and self.music_player.isAlive():
            self.music_player.cancelplaying()
class SystemCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        os.system(' '.join(cmd))
class HomeAuth():
    def __init__(self,key_path,email):
        self.key_path = key_path
        self.email = email
        self.dropbox = myDropbox()
        self.pub = ''
        self.camera = CameraCmd()
        self.screen = ScreenCmd()
        self.audio  = AudioCmd()
        self.syscmd = SystemCmd()
        self.cmdpro = {'system':self.syscmd,'camera':self.camera,'screen':self.screen,'audio':self.audio}
    def getCmd(self):      
        if not self.pub:
            f = requests.get(common.SERVER_PUBKEY_URL,proxies=common.PROXY)
            self.pub = f.text
        pubkey = RSA.importKey(self.pub)
        with open(self.key_path) as f:
            privkey = RSA.importKey(f.read())
        sig = Crypto.Random.new().read(16)
        info = str(len(self.email))+self.email+sig
        signature = privkey.sign(sig,'')
        encinfo = pubkey.encrypt(info,32)
        para=({'signature':repr(signature),'userinfo':repr(encinfo)})
        urllib.urlencode(para)
        r = requests.post(common.SERVER_CMD_URL,data=para,proxies=common.PROXY)
        logging.debug(r.json())
        return r.json()
    def handleCmd(self):
        t = common.REQUESTS_TIME
        while True:
            try:
                cmd = self.getCmd()
            except Exception,data:
                logging.error(data)
                t = 2* t
            else:
                if cmd['err'] == 'ok' and cmd['response']['new'] == True:
                    logging.debug(cmd['response']['cmdline'])
                    cmdline = cmd['response']['cmdline'].strip().split()
                    try:
                        self.cmdpro[cmdline[0]].runCmd(cmdline[1:])
                    except Exception,data:
                        logging.error(data)
                    t = common.REQUESTS_TIME
            finally:
                time.sleep(t)
        
def main():
    logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')
    h = HomeAuth(os.path.join(ROOT_DIR,'id_rsa'),common.USER_EMAIL.strip())
    h.handleCmd()
if __name__=='__main__':
    main()
