import re
import pywikibot
from pywikibot import pagegenerators

site = pywikibot.Site()

gen = pagegenerators.RecentChangesPageGenerator(
    total=500, topOnly=True, namespaces=0, showRedirects=False)


def getEnglishTokenV2(string):
    with open("items_english.txt", encoding="utf16") as english_items:
        for line in english_items:
            line = line.rstrip()

            if string in line:
                regex = re.compile("\"(.[^\"]+)\"[\t\s]+\"(.[^\"]+)\"")
                matches = re.finditer(regex, line)

                for match in matches:
                    if match and match.group(2) == string:
                        if "DOTA_Item_" in match.group(1) or "DOTA_Tooltip_Ability_item_" in match.group(1):
                            return match.group(1)
                        else:
                            break
    english_items.close()


def getTranslatedStringV2(token, original):
    with open("items_brazilian.txt", encoding="utf16") as translated_items:
        for line in translated_items:
            line = line.rstrip()

            if type(token) is str:
                if token in line:
                    regex = re.compile("\"(.[^\"]+)\"[\t\s]+\"(.[^\"]+)\"")
                    matches = re.finditer(regex, line)

                    for match in matches:
                        if match and match.group(1) == token:
                            return match.group(2)
            else:
                return original

    translated_items.close()


for page in gen:
    if "{{I|" in page.text or "{{Cosmetic|" in page.text:
        textOld = page.text
        text = page.text

        for line in text.splitlines():
            if "{{I|" in line or "{{Cosmetic|" in line:
                regexNoSize = re.compile("\{\{(I|Cosmetic)\|([^}]+)\}\}")
                regexHasSize = re.compile(
                    "\{\{(I|Cosmetic)\|([^}]+)\|([\d]+)px\}\}")
                matchesNoSize = re.finditer(regexNoSize, line)
                matchesHasSize = re.finditer(regexHasSize, line)

                for match in matchesHasSize:
                    template = match.group(1)
                    itemOriginal = match.group(2)

                    # if "Tango" not in itemOriginal:
                    itemTranslation = getTranslatedStringV2(
                        getEnglishTokenV2(itemOriginal), itemOriginal)
                    itemImage = match.group(3)

                    if itemTranslation:
                        text = text.replace(
                            "{{%s|%s|%spx}}" % (
                                template, itemOriginal, itemImage),
                            "{{%s|%s|%spx}}" % (
                                template, itemTranslation, itemImage)
                        )

                for match in matchesNoSize:
                    template = match.group(1)
                    itemOriginal = match.group(2)

                    # if "Tango" != itemOriginal and "Tango" not in itemOriginal:
                    itemTranslation = getTranslatedStringV2(
                        getEnglishTokenV2(itemOriginal), itemOriginal)

                    if itemTranslation:
                        text = text.replace(
                            "{{%s|%s}}" % (template, itemOriginal),
                            "{{%s|%s}}" % (template, itemTranslation)
                        )

        if textOld == text:
            print("Não atualizando %s porque não temos nomes." % page)
        else:
            page.text = u"" + text + ""
            page.save(u"Auto: Tradução automática de nomes de itens")

            print("Atualizando %s com nomes traduzidos." % page)
