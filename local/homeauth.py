#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests,os.path,urllib,logging,time,subprocess,json,threading
from Crypto.PublicKey import RSA
import Crypto.Random
logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')
ROOT_DIR = os.path.dirname(__file__)
class DoubanFM():
    def __init__(self):
        self.logined = False
        self.history = []
        self.song_list = []
        self.channel = 1
        self.cur_song = {'sid':''}
#        self.proxy = {'http':'http://127.0.0.1:9341'}
        self.proxy = None
    def login(self,email,passwd):
        payload={'email':email,'password':passwd,'app_name':'radio_desktop_win','version':100}
        url = 'http://www.douban.com/j/app/login'
        r = requests.post(url, data=payload,proxies=self.proxy)
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
        r = requests.get(url,params=payload,proxies=self.proxy)
        return r.json()['song']
    def getChannels(self):
        url = 'http://www.douban.com/j/app/radio/channels'
        r = requests.get(url,proxies=self.proxy)
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
        self.songnum = songnum
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
        pro = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            pro.communicate()
        except Exception,e:
            pro.terminate()
    def cancelplaying(self):
        self.cancelplay = True
class myDropbox():
    def __init__(self):
        pass
    def createFolder(self,path):
        pass
    def uploadFile(self,upfile,tofile):
        pass
class CameraCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        logging.debug(cmd)
class ScreenCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        logging.debug(cmd)
class AudioCmd():
    def __init__(self):
        self.music_player = None
    def runCmd(self,cmd):
        logging.debug(cmd)
        cmd = cmd.lower()
        if len(cmd) <= 1 or cmd[0] != 't':
            logging.error('old cmd')
            return
        if cmd[1] == 'p':#play
            if self.music_player is None or not self.music_player.isAlive():
                try:
                    n = int(cmd[2:])
                    self.music_player = MusicPlayer(n)
                    self.music_player.start()
                except Exception,d:
                    logging.error(d)
                    return
        elif cmd[1] == 's':#stop
            if self.music_player is not None and self.music_player.isAlive():
                self.music_player.cancelplaying()
        else:
            logging.error('invalid cmd')
class HomeAuth():
    def __init__(self,key_path,email):
        self.key_path = key_path
        self.email = email
        self.dropbox = myDropbox()
    def getCmd(self):      
        f = requests.get('http://homeauth-lsjustin.dotcloud.com/static/key/id_rsa.pub')
        pub = f.text
        pubkey = RSA.importKey(pub)
        with open(self.key_path) as f:
            privkey = RSA.importKey(f.read())
        sig = Crypto.Random.new().read(16)
        info = str(len(self.email))+self.email+sig
        signature = privkey.sign(sig,'')
        encinfo = pubkey.encrypt(info,32)
        para=({'signature':repr(signature),'userinfo':repr(encinfo)})
        urllib.urlencode(para)
        r = requests.post('http://homeauth-lsjustin.dotcloud.com/handlecmd/getcmd/',data=para)
        logging.debug(r.json())
        return r.json()
    def handleCmd(self):
        camera = CameraCmd()
        screen = ScreenCmd()
        audio  = AudioCmd()
        while True:
            cmd = self.getCmd()
            if cmd['err'] == 'ok' and cmd['response']['new'] == True:
                camera.runCmd(cmd['response']['camera_cmd'])
                screen.runCmd(cmd['response']['screen_cmd'])
                audio.runCmd(cmd['response']['audio_out_cmd'])
#            break
            time.sleep(5)
        
def main():
    h = HomeAuth(os.path.join(ROOT_DIR,'id_rsa'),'lsjustin@yeah.net')
    h.handleCmd()
if __name__=='__main__':
    main()
