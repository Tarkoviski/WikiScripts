# -*- coding: utf-8 -*-
import pywikibot
from apscheduler.schedulers.blocking import BlockingScheduler
import feedparser
import re
import requests
from bs4 import BeautifulSoup

site = pywikibot.Site()

def checkblog():
    d = feedparser.parse('http://br.dota2.com/feed/')
    link = d['entries'][0]['link'] 
    title = d['entries'][0]['title']
    pub = d['entries'][0]['published']
    pubS = pub.split(" ")

    monthNum = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }

    pubdate = "blog-data = %s-%s-%s" % (pubS[3], monthNum[pubS[2]], pubS[1])

    f = open("blog.txt", "r")
    if f.readline() == title:
        print("Blog igual. Ignorando...")
    else:
        print("Atualizando blog....")
        f2 = open("blog.txt", "w") 
        f2.write(title)
        f2.close() 
        page = pywikibot.Page(site, u"Predefinição:Updates")
        text = page.text
        regexDate = '(blog-data = (201[1-9])-([0-9][0-9])-([0-9][0-9]))'
        regex = '(http:\/\/br.dota2.com([-a-zA-Z0-9@:%_\+.~#?&//=]*))'
        atualiza = re.sub(regex, link, text)
        atualiza = re.sub(regexDate, pubdate, atualiza)
        pubSummary = "Auto: Nova publicação no Blog: \"%s\"" % title
        page.text = u'' + atualiza + ''
        page.save(u"" + pubSummary + "")
        print(pubSummary)

    f.close()

def checkupdated():
    page = requests.get("http://www.dota2.com/news/updates/")
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        updates = soup.find_all("div", class_="recent_entry")

        updateDate = updates[0].find('div', attrs={'class': 'recent_entry_date'}).text

        monthNum = {
            "Jan.": "01",
            "Feb.": "02",
            "Mar.": "03",
            "Apr.": "04",
            "May.": "05",
            "Jun.": "06",
            "Jul.": "07",
            "Aug.": "08",
            "Sep.": "09",
            "Oct.": "10",
            "Nov.": "11",
            "Dec.": "12"
            }

        updateMonth = updateDate.split(" ")[0]
        updateDay = updateDate.split(" ")[1]
        updateYear = updateDate.split(" ")[2]
        updateFull = "%s-%s-%s" % (updateYear, monthNum[updateMonth], updateDay.replace(",", ""))

        currentDate = pywikibot.Page(site, u"Predefinição:Updates/Last")
        currentDatetext = currentDate.text

        datewiki = currentDatetext
        dateblog = updateFull

        print("BLOG: " + dateblog + " | WIKI: " + datewiki)

        if datewiki == dateblog:
            print("Igual ao blog")
        else:
            print("Diferente do blog")
            if datewiki > dateblog:
                print("Wiki é mais recente (W:% - B:%)")
            else:
                print("Blog maior (W:% - B:%). Vamos atualizar!")
                page = pywikibot.Page(site, u"Predefinição:Updates/Last")
                page.text = u'' + dateblog + ''
                page.save(u"Auto: Atualizando data da última atualização.")
                print("Wiki atualizada para " + dateblog)


scheduler = BlockingScheduler()
scheduler.add_job(checkblog, 'interval', minutes=30)
scheduler.add_job(checkupdated, 'interval', minutes=30)
scheduler.start()