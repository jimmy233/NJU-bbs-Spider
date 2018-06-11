#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

class Card:
    def __init__(self):
        self.sequence = ''
        self.state = ''
        self.author = ''
        self.date = ''
        self.title = None
        self.url = ''
    def __str__(self):
        return "sequence: " + self.sequence + " state: " + self.state  + " author: " +  self.author +  " date: " +  self.date +  " title: " + self.title.text + " url: " + self.url


class BBSSpider:
    def __init__(self):
        self.host = "http://bbs.nju.edu.cn"
        self.boardURL = self.host + '/board'
        self.userURL = self.host + '/blogdoc'
        self.forum_dict = {
            '就业特快': 'JobExpress',
            '失物招领': 'LostToFind',
            '读书': 'Reading',
            '计算机系': 'D_Computer',
            '女生天地': 'Girls'
        }
    #返回具体数据的tableContent。类型为'bs4.element.Tag'
    def get_forum_content(self, forum):
        """
        返回forum版块中数据

        Arguments:
            forum: 版块信息.

        Returns:
            list<Card>
        """
        forum_key = self.forum_dict[forum]
        response = requests.get(self.boardURL, params={"board": forum_key})
        with open("forum_info.html", "w") as f:
            f.write(response.text)
            print("succeed to grab content")
        soup = BeautifulSoup(response.text, "lxml")
        #取得数据的table
        tableContent = soup.findAll('table')[3]
        #print(soup.findAll('table')[3])
        cards = self.__get_forum_cards(tableContent)
        return cards


    def get_user_content(self, userid):
        """
        返回该用户的发帖数据表格

        Arguments:
            userid: 用户id

        Returns:
            tableContent<bs4.element.Tag>
        """
        response = requests.get(self.userURL, params={'userid': userid})
        with open('user_info.html', 'w') as f:
            f.write(response.text)
            print('succeed to grab content')
        soup = BeautifulSoup(response.text, "lxml")
        #取得数据的table
        tableContent = soup.findAll('table')[3]
        #print(tableContent)
        cards = self.__get_user_cards(userid, tableContent)
        return cards


    def __get_forum_cards(self, tableContent):
        """
        对table进行处理，得到数据列表

        Returns:
            list<Card>
        """
        #得到所有的rows
        trs = tableContent.findAll('tr')
        #去掉第一行， 开始生成dict
        cards = []
        for tr in trs[1:]:
            card = Card()
            tds = tr.find_all('td')

            card.sequence = tds[0].text
            card.state = tds[1].text
            card.author = tds[2].text
            card.date = tds[4].text[:12]
            card.title = tds[5]
            #print("title ", card.title)
            card.url = self.host + "/" + card.title.a["href"]

            cards.append(card)
        return cards
    

    def __get_user_cards(self, userid, tableContent):
        """
        对table进行处理，得到数据列表

        Returns:
            list<Card>
        """
        #得到所有的rows
        trs = tableContent.findAll('tr')
        #去掉第一行， 开始生成dict
        cards = []
        for tr in trs[1:]:
            card = Card()
            tds = tr.find_all('td')
            card.sequence = tds[0].text
            card.date = tds[1].text
            card.author = userid
            card.title = tds[2]
            card.url = self.host + "/" + card.title.a["href"]

            cards.append(card)
        return cards


if __name__ == '__main__':
    bbs = BBSSpider()
    print('start to test forum: 就业特快')
    cards = bbs.get_forum_content('就业特快')
    print('len cards: ', len(cards))
    print('the last card: ', cards[-1])
    print('start to test user cards: wang 360')
    cards = bbs.get_user_content('wang360')
    print("len cards: ", len(cards))
    print('the last card: ', cards[-1])
