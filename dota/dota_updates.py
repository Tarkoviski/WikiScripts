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
siteEn = pywikibot.Site("en", "dotawiki")

templateURLEn = u"Template:Updates"
templateURLPt = u"Predefinição:Updates"

# Verificamos a o blog oficial para buscar por novas publicações


def checkblog():
    blogFeed = feedparser.parse("http://br.dota2.com/feed/")
    blogLastEntryLink = blogFeed["entries"][0]["link"]
    blogLastEntryTitle = blogFeed["entries"][0]["title"]
    blogLastEntryPublised = blogFeed["entries"][0]["published"]
    blogLastEntryPublisedDate = blogLastEntryPublised.split(" ")

    monthNumbers = {
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

    blogFile = open("blog.txt", "r")
    currentBlog = blogFile.readline()
    blogFile.close()

    if currentBlog != blogLastEntryTitle:
        print("BLOG: Blog difere (Wiki: %s - Blog: %s)" %
              (currentBlog, blogLastEntryTitle))

        # Podiamos usar um banco de dados aqui
        # Ou achar uma forma melhor de salvar isso que num arquivo de texto
        blogFile2 = open("blog.txt", "w")
        blogFile2.write(blogLastEntryTitle)
        blogFile2.close()

        page = pywikibot.Page(site, templateURLPt)
        pageText = page.text

        regexBlogDate = "(blog-data = ([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9]))"
        regexBlogURL = "(https?:\/\/br.dota2.com([-a-zA-Z0-9@:%_\+.~#?&//=]*))"

        newTextBlogURL = re.sub(regexBlogURL, blogLastEntryLink, pageText)
        newTextBlogDate = re.sub(regexBlogDate, "blog-data = %s-%s-%s" % (
            blogLastEntryPublisedDate[3], monthNumbers[blogLastEntryPublisedDate[2]], blogLastEntryPublisedDate[1]), newTextBlogURL)

        page.text = u"" + newTextBlogDate + ""
        page.save(u"Auto: Nova publicação no Blog: \"%s\"" % blogLastEntryTitle)

        print("BLOG: Blog atualizado para %s (era %s)" % (blogLastEntryTitle, currentBlog))


# Mesma coisa que a função anterior, só que para as atualizações recentes


def checkupdated():
    updatesPageEn = pywikibot.Page(siteEn, templateURLEn)
    updatesPageEn = updatesPageEn.text

    updatesPagePt = pywikibot.Page(site, templateURLPt)
    updatesPagePtText = updatesPagePt.text

    regexVersion = "(versão = ([0-9][0-9]|[0-9])\.[0-9][0-9].?)"
    regexVersionDate = "(versão-data = ([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9]))"
    regexPatchDate = "(atualização-data = ([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9]))"
    regexPatchDateTest = "(atualização-data-test = ([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9]))"

    for line in updatesPageEn.splitlines():
        if line.startswith("| version = "):
            versionNumber = line.split(" = ")[1]
        elif line.startswith("| version-date = "):
            versionDate = line.split(" = ")[1]
        elif line.startswith("| patch-date = "):
            patchDate = line.split(" = ")[1]
        elif line.startswith("| test-patch-date = "):
            patchDateTest = line.split(" = ")[1]

    for line in updatesPagePtText.splitlines():
        if line.startswith("| versão = "):
            currentVersionNumber = line.split(" = ")[1]
        elif line.startswith("| versão-data = "):
            currentVersionDate = line.split(" = ")[1]
        elif line.startswith("| atualização-data = "):
            currentPatchDate = line.split(" = ")[1]
        elif line.startswith("| atualização-data-test = "):
            currentPatchDateTest = line.split(" = ")[1]

    if currentPatchDate != patchDate:
        print("ATUALIZAÇÃO: Data de atualização difere (PT: %s - EN: %s)" %
              (currentPatchDate, patchDate))

        page = pywikibot.Page(site, templateURLPt)
        pageText = page.text

        newTextPatchDate = re.sub(regexPatchDate, "atualização-data = " +
                                  patchDate, pageText)

        page.text = (u"" + newTextPatchDate + "")
        page.save(u"Auto: Atualizando data da última atualização.")

        print("ATUALIZAÇÃO: Data da última atualização atualizada para %s (era %s)" %
              (patchDate, currentPatchDate))
    elif currentVersionNumber != versionNumber or currentVersionDate != versionDate:
        print("Versão difere (PT: %s - EN: %s)" % (currentVersionNumber, versionNumber))

        page = pywikibot.Page(site, templateURLPt)
        pageText = page.text

        newTextVersionNumber = re.sub(regexVersion, "versão = " + versionNumber, pageText)
        newTextVersionDate = re.sub(regexVersionDate, "versão-data = " +
                                    versionDate, newTextVersionNumber)

        page.text = (u"" + newTextVersionDate + "")
        page.save(u"Auto: Atualizando versão.")

        print("ATUALIZAÇÃO: Versão atualizada para %s (era %s)" %
              (patchDateTest, currentPatchDateTest))
    elif currentPatchDateTest != patchDateTest:
        print("ATUALIZAÇÃO: Data de atualização (Test) difere (PT: %s - EN: %s)" %
              (currentPatchDateTest, patchDateTest))

        page = pywikibot.Page(site, templateURLPt)
        pageText = page.text

        newTextPatchDateTest = re.sub(regexPatchDateTest, "atualização-data-test = " +
                                      patchDateTest, pageText)

        page.text = (u"" + newTextPatchDateTest + "")
        page.save(u"Auto: Atualizando data da última atualização (Test).")

        print("ATUALIZAÇÃO: Data da última atualização (Test) atualizada para %s (era %s)" %
              (patchDateTest, currentPatchDateTest))

# Atualizamos a nossa presença
# Isso é usado mais como uma forma de verificação para ver se o bot ainda está funcionando corretamente


def updatepresence():
    lastBeat = pywikibot.Page(site, u"User:Espacorede/Beat")
    lastBeatDate = lastBeat.text
    today = str(strftime("%Y-%m-%d", gmtime()))

    if lastBeatDate != today:
        print("PRESENÇA: Atualizando presença")
        page = pywikibot.Page(site, u"User:Espacorede/Beat")
        page.text = u"" + today + ""
        page.save(u"Auto: Atualizando presença.")


scheduler = BlockingScheduler()
scheduler.add_job(checkblog, "interval", minutes=30)
scheduler.add_job(checkupdated, "interval", minutes=5)
scheduler.add_job(updatepresence, "interval", days=1)
scheduler.start()
