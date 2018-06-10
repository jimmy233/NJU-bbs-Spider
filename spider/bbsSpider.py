#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

class Card:
    def __init__(self):
        self.sequence = None
        self.state = None
        self.author = None
        self.date = None
        self.title = None
        self.url = None
    def __str__(self):
        return "sequence: " + self.sequence + " state: " + self.state + " author: " +  self.author.text +  " date: " +  self.date +  " title: " + self.title.text + " url: " + self.url


class BBSSpider:
    def __init__(self):
        self.host = "http://bbs.nju.edu.cn"
        self.boardURL = self.host + "/board"
        self.jobExpress = "Jobexpress"  

    #返回具体数据的tableContent。类型为'bs4.element.Tag'
    def getJobExpress(self):
        """
        返回就业特快版中数据表格

        Returns:
            tableContent<bs4.element.Tag>
        """
        response = requests.get(self.boardURL, params={"board": self.jobExpress})
        with open("jobexpress.html", "w") as f:
            f.write(response.text)
            print("succeed to grab content")
        soup = BeautifulSoup(response.text, "lxml")
        #取得数据的table
        tableContent = soup.findAll('table')[3]
        #print(soup.findAll('table')[3])
        return tableContent

    def getCards(self, tableContent):
        """
        对table进行处理，得到数据列表

        Returns:
            dict<Card>
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
            card.author = tds[2]
            card.date = tds[4].text[:12]
            card.title = tds[5]
            #print("title ", card.title)
            card.url = self.host + "/" + card.title.a["href"]
            print(card)

            cards.append(card)
        return cards
if __name__ == '__main__':
    bbs = BBSSpider()
    tableContent = bbs.getJobExpress()
    cards = bbs.getCards(tableContent)
    print("len cards: ", len(cards))
