#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:26:53 2018

@author: jimmy233
"""

import itchat
import requests
import bbsSpider
import time  
import threading 
from itchat.content import *

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or defaultReply
#@itchat.msg_register(TEXT)   #这里的TEXT表示如果有人发送文本消息，那么就会调用下面的方法
@itchat.msg_register(itchat.content.TEXT)
def simple_reply(msg):
    #这个是向发送者发送消息
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    nick=msg_from
    print(msg['Text'])
    st=msg['Text']
    if st=='我要关注':
       itchat.send_msg('http://127.0.0.1:8080/test?id=%s'%nick,toUserName=msg['FromUserName'])
    else:
       itchat.send_msg(tuling_reply(msg),toUserName=msg['FromUserName'])
    #itchat.send_msg('已经收到了文本消息，消息内容为%s'%msg['Text'],toUserName=msg['FromUserName'])
    #return "不想理你，并觉得你很傻逼"#"T reveived: %s" % msg["Text"]     #返回的给对方的消息，msg["Text"]表示消息的内容
def t1():
    itchat.run()
def t2():
    author = itchat.search_friends(nickName='明月无晴')[0]
    bbs = bbsSpider.BBSSpider()
    tableContent = bbs.getJobExpress()
    cards = bbs.getCards(tableContent)
    author.send("memeda")
    print(author)
itchat.auto_login()
threads = []
th1 = threading.Thread(target=t1, args=())
th1.start()
threads.append(th1)
th2 = threading.Thread(target=t2, args=())
th2.start()
threads.append(th2)
for th in threads:  
    th.join()

