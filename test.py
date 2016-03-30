#!/usr/bin/python 
#-*- coding: UTF-8 -*- 

import csv
import json
# import urllib
import urllib2
import re
from bs4 import BeautifulSoup



class User:
    def __init__(self, sid, username, link):
        self.sid = sid
        self.username = None
        self.siteURL = link
        self.articles_list = []
        self.articles = []

        print 'getting page:' + link
        request = urllib2.Request(link)
        response = urllib2.urlopen(request)

        try:
            soup = BeautifulSoup(response, "html.parser")
            # self.username = soup.select('.site-title')[0].get_text()
            for entry in soup.select('.entry-title'):
                self.articles_list.append(entry.a['href'])
        except Exception, e:
            print e
    # def __str__(self):

    def getArticles(self):
        for i in range(len(self.articles_list)):
            if i == 3:
                break
            try:
                response = urllib2.urlopen(self.articles_list[i])
                soup = BeautifulSoup(response, "html.parser")
                artical = {}
                title = soup.select('.entry-title')[0].get_text()
                artical['title'] = title
                ps = soup.select('.entry-content > p')
                content = ""
                for p in ps:
                    content += p.get_text()
                artical['content'] = content
                comments = soup.select('.comment-list > li')
                artical['comments'] = []
                artical['url'] = self.articles_list[i]
                for c in comments:
                    comment = {}
                    comment['from'] = str(c.b.get_text()).strip()
                    comment['to'] = self.username
                    edges.append((comment['from'], comment['to']))
                    comment['content'] = c.p.get_text().strip()
                    comment['time'] = c.time.get_text().strip()
                    artical['comments'].append(comment)
                self.articles.append(artical)
            except Exception, e:
                print e
                continue
            # print '\n\n'
                
            
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


users = [None] * 100
j = 0
edges = []
with open('IEMS5723_Blog_URLs.csv', 'rb') as usersfile:
    reader = csv.reader(usersfile, delimiter=',')
    headers = next(reader)
    for row in reader:
        sid, username, link = row[2], row[3], row[4]
        users[j] = User(sid, username, link)
        users[j].getArticles()
        j += 1

with open('edges.txt', 'wb') as wf:
    for e in edges:
        wf.write(e[0] + ' ' + e[1] + '\n')

uf = open('users.txt', 'wb')
for i in range(100):
    if users[i]:
        uf.write(users[i].to_JSON())
    else:
        break
# print users[0].id
# print users[0].articles_list
# userlinks = ['https://ypzheng.wordpress.com/', 'https://tidetam.wordpress.com/']
# users = [User(l) for l in userlinks]
# print users[0].articles_list
# print users[1].articles_list

        # page = self.getPage()
        # pattern = re.compile('<h1 class="entry-title"><a href="(.*?)".*')
        # items = re.findall(pattern,page)
        # for item in items:
        #     print item

 