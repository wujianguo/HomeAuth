#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests,os.path,urllib
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import Crypto.Random
def certify():
    privf=os.path.join(os.path.dirname(os.path.realpath(__file__)),'id_rsa')
    pubf = os.path.join(os.path.dirname(os.path.realpath(__file__)),'id_rsa.pub')
    f=open(privf,'rb')
    privkey=RSA.importKey(f.read())
    f.close()
    f=open(pubf,'rb')
    pubkey=RSA.importKey(f.read())
    f.close()
    text=MD5.new(Crypto.Random.get_random_bytes(128)).digest()    
    signature=privkey.sign(text,'')
    print(pubkey.verify(text,signature))
def testHomeauth():
    f = requests.get('http://homeauth-lsjustin.dotcloud.com/static/key/id_rsa.pub')
    pub = f.text
#    print(pub)
    pubkey = RSA.importKey(pub)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'id_rsa')) as f:
        privkey = RSA.importKey(f.read())
    sig = 'abc'
    info = '17lsjustin@yeah.net'+sig
    signature = privkey.sign(sig,'')
    encinfo = pubkey.encrypt(info,32)
    para=({'signature':repr(signature),'userinfo':repr(encinfo)})
#    para=({'signature':'d','userinfo':'a'})
    urllib.urlencode(para)
#    print(para)
    r = requests.post('http://homeauth-lsjustin.dotcloud.com/handlecmd/getcmd/',data=para)

    s=r.json()
    print(s)
def main():
#    certify()
    testHomeauth()
if __name__=='__main__':
    main()
