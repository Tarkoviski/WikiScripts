# -*- coding: utf-8 -*-
import pywikibot
from apscheduler.schedulers.blocking import BlockingScheduler
import feedparser
import re
import requests
import time
from time import gmtime, strftime
from bs4 import BeautifulSoup

site = pywikibot.Site()

# Verificamos a o blog oficial para buscar por novas publicações
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
    if f.readline() != title:
        print("BLOG: Atualizando blog")
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

    f.close()

# Mesma coisa que a função anterior, só que para as atualizações recentes
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

        if datewiki != dateblog:
            datewikisafe = time.strptime(datewiki, "%Y-%m-%d")
            dateblogsafe = time.strptime(dateblog, "%Y-%m-%d")
            if datewikisafe > dateblogsafe:
                # Algumas atualizações não são documentadas no blog oficial, não vamos sobrescrever isso
                print("ATUALIZAÇÃO: Wiki é mais recente (W:%s - B:%s)" % (datewiki, dateblog))
            else:
                page = pywikibot.Page(site, u"Predefinição:Updates/Last")
                page.text = u'' + dateblog + ''
                page.save(u"Auto: Atualizando data da última atualização.")
                print("ATUALIZAÇÃO: Data atualizada para %s" % dateblog)

# Atualizamos a nossa presença
# Isso é usado mais como uma forma de verificação para ver se o bot ainda está funcionando corretamente
def updatepresence():
    lastBeat = pywikibot.Page(site, u"User:Espacorede/Beat")
    lastBeatDate = lastBeat.text
    today = str(strftime("%Y-%m-%d", gmtime()))

    if lastBeatDate != today:
        print("PRESENÇA: Atualizando presença")
        page = pywikibot.Page(site, u"User:Espacorede/Beat")
        page.text = u'' + today + ''
        page.save(u"Auto: Atualizando presença.")
 
scheduler = BlockingScheduler()
scheduler.add_job(checkblog, 'interval', minutes=1)
scheduler.add_job(checkupdated, 'interval', minutes=1)
scheduler.add_job(updatepresence, 'interval', days=1)
scheduler.start()