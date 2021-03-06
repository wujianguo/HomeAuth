#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import getopt,logging
import threading,subprocess
from settings import *
log = logging.getLogger('audio')
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
        r = requests.post(url, data=payload,proxies=PROXY)
        data = r.json()
        if data['err']!='ok':
            log.error('login failed')
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
        log.debug('%s %s'%(song['artist'],song['title']))
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
        r = requests.get(url,params=payload,proxies=PROXY)
        return r.json()['song']
    def getChannels(self):
        url = 'http://www.douban.com/j/app/radio/channels'
        r = requests.get(url,proxies=PROXY)
        return r.json()['channels']
    def printChannels(self):
        self.channels = ''
        if not self.channels:
            self.channels = self.getChannels()
        for channel in self.channels:
            log.info('%d\t%s\t%s'%(channel['channel_id'],channel['name'],channel['name_en']))
class MusicPlayer(threading.Thread):
    def __init__(self,songnum):
        super(MusicPlayer, self).__init__(cmd_queue)
        self.doubanFM = DoubanFM()
        self.cancelplay = False
        self.pro = None
        self.cmd_queue = cmd_queue
    def run(self):
        while True:
            cmd = self.cmd_queue.get()
            log.debug(cmd)
            optlist,args = getopt.getopt(cmd,'p:s')
            for o,v in optlist:
                if o == '-p':
                    try:
                        self.playSongs(int(v))
                    except Exception,data:
                        log.error(data)
                if o == '-s':
                    self.cancelplaying()
    def playSongs(self,songnum):
        if songnum < 0:
            return
        while True:
            song = self.doubanFM.playSong()
            self.playing(song['url'])
            songnum = songnum - 1
            if songnum == 0 or self.cancelplay:
                break
        self.cancelplay = False
    def playing(self,url):
        cmd = ['ffplay',url,'-nodisp','-autoexit']
        self.pro = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            self.pro.communicate()
        except Exception,data:
            log.error(data)
            if self.pro.returncode is None:
                self.pro.terminate()
    def cancelplaying(self):
        self.cancelplay = True
        if self.pro and self.pro.returncode is None:
            self.pro.terminate()
class AudioCmd():
    music_player = None
    @staticmethod
    def runCmd(cmd):
        log.debug(cmd)
        optlist,args = getopt.getopt(cmd,'p:s')
        for o,v in optlist:
            if o == '-p':
                if not AudioCmd.isPlaying():
                    try:
                        AudioCmd.music_player = MusicPlayer(v)
                        AudioCmd.music_player.start()
                    except Exception,data:
                        log.error(data)
            if o == '-s':
                AudioCmd.terminate()
    @staticmethod
    def terminate():
        if AudioCmd.isPlaying():
            AudioCmd.music_player.cancelplaying()
    @staticmethod
    def isPlaying():
        if AudioCmd.music_player is not None and AudioCmd.music_player.isAlive():
            return True
        else:
            return False
            