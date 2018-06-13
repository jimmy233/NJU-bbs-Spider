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
#import urllib3
import json
import base64
#import requests
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
    nick=base64.b64encode(bytes(msg_from,encoding='utf-8'))
    print(msg['Text'])
    st=msg['Text']
    if st=='我要关注':
       itchat.send_msg('http://118.25.190.133:8080/test?id=%s'%str(nick,encoding='utf-8'),toUserName=msg['FromUserName'])
    else:
       itchat.send_msg(tuling_reply(msg),toUserName=msg['FromUserName'])
    #itchat.send_msg('已经收到了文本消息，消息内容为%s'%msg['Text'],toUserName=msg['FromUserName'])
    #return "不想理你，并觉得你很傻逼"#"T reveived: %s" % msg["Text"]     #返回的给对方的消息，msg["Text"]表示消息的内容
def forum(hjson,bbs,sequence_len,Max_sequence):
        forum_length=len(hjson['forum'])
        if forum_length > sequence_len:
            for t in range(sequence_len,forum_length):
                Max_sequence[hjson['forum'][t]]=-1
            sequence_len=forum_length
        for key in hjson['forum']:
            forum_name=key
            #print("233"+key)
            cards = bbs.get_forum_content(forum_name)
            cards_length = len(cards)
            last_sequence = int(cards[-1].sequence)
            if last_sequence > Max_sequence[key]:
                if Max_sequence[key] == -1:
                    for user in hjson['forum'][key]:
                        user = str(base64.b64decode(bytes(user,encoding='utf-8')),encoding = 'utf-8')
                        print(itchat.search_friends(nickName=user))
                        author = itchat.search_friends(nickName=user)[0]
                        if cards_length > 5:
                            for i in range(1,6):
                                print(cards[-i])
                                st=cards[-i].display()
                                author.send(st)
                        elif cards_length>0 and cards_length<=5:
                            for j in range(1,cards_length):
                                st=cards[-i].display()
                                author.send(st)
                        elif cards_length == 0 :
                                author.send("Sorry, 您关注的板块无信息")                    
                else:
                    num= last_sequence - Max_sequence[key]
                    #print("2333:"+num)
                    for user in hjson['forum'][key]:
                        author = itchat.search_friends(nickName=user)[0]
                        for i in range(1,num+1):
                            print(cards[-i])
                            st=cards[-i].display()
                            author.send("新的消息:"+'\n'+st)
            Max_sequence[key] = last_sequence
def user(hjson,bbs,sequence_len,Max_sequence):
        user_length=len(hjson['user'])
        if user_length > sequence_len:
            for t in range(sequence_len,user_length):
                Max_sequence[hjson['user'][t]]=-1
            sequence_len=user_length
        for key in hjson['user']:
            user_name=key
            #print("233"+key)
            cards = bbs.get_forum_content(user_name)
            cards_length = len(cards)
            last_sequence = int(cards[-1].sequence)
            if last_sequence > Max_sequence[key]:
                if Max_sequence[key] == -1:
                    for userId in hjson['user'][key]:
                        userId = str(base64.b64decode(bytes(userId,encoding='utf-8')),encoding = 'utf-8')
                        author = itchat.search_friends(nickName=userId)[0]
                        if cards_length > 5:
                            for i in range(1,6):
                                print(cards[-i])
                                st=cards[-i].display()
                                author.send(st)
                        elif cards_length>0 and cards_length<=5:
                            for j in range(1,cards_length):
                                st=cards[-i].display()
                                author.send(st)
                        elif cards_length == 0 :
                                author.send("Sorry, 您关注的板块无信息")                    
                else:
                    num= last_sequence - Max_sequence[key]
                    #print("2333:"+num)
                    for user in hjson['forum'][key]:
                        author = itchat.search_friends(nickName=user)[0]
                        for i in range(1,num+1):
                            print(cards[-i])
                            st=cards[-i].display()
                            author.send("新的消息:"+'\n'+st)
            Max_sequence[key] = last_sequence
def t1():
    itchat.run()
def t2():
    #author = itchat.search_friends(nickName='明月无晴')[0]
    url='http://118.25.190.133:8080/getdict'
    #http_init = urllib3.PoolManager()
    response_init = requests.get(url)
    print(response_init.text)
    hjson_init = json.loads(response_init.text)
    Max_sequence_forum = {}
    Max_sequence_user = {}
    for key in hjson_init['forum']:
        Max_sequence_forum[key]=-1
    for key in hjson_init['user']:
        Max_sequence_user[key]=-1
    sequence_len_forum=len(Max_sequence_forum)
    sequence_len_user=len(Max_sequence_user)
    while True:
        bbs = bbsSpider.BBSSpider()
        #http = urllib3.PoolManager()
        response = requests.get(url)
        hjson = json.loads(response.text) 
        forum(hjson,bbs,sequence_len_forum,Max_sequence_forum)
        user(hjson,bbs,sequence_len_user,Max_sequence_user)
        time.sleep(15)
            
                        
                        
itchat.auto_login(hotReload=True,enableCmdQR=2)
threads = []
th1 = threading.Thread(target=t1, args=())
th1.start()
threads.append(th1)
th2 = threading.Thread(target=t2, args=())
th2.start()
threads.append(th2)
for th in threads:  
    th.join()

