import re
import pywikibot
from pywikibot import pagegenerators
import wikitextparser as wtp

site = pywikibot.Site()

cat = pywikibot.Category(site, "Categoria:Itens cosméticos")
gen = pagegenerators.CategorizedPageGenerator(cat)

def getEnglishTokenV2(string):
    with open("items_english.txt", encoding="utf8") as english_items:
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
    with open("items_brazilian.txt", encoding="utf8") as translated_items:
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


def getTranslatedItems(content):
    textOld = content
    text = content

    # Todo: Use wikitextparser
    if "{{I|" in content or "{{Cosmetic|" in content or "[[" in content:
        for line in text.splitlines():
            if "{{I|" in line or "{{Cosmetic|" in line or "[[" in line:
                regexNoSize = re.compile("\{\{(I|Cosmetic)\|([^}]+)\}\}")
                regexHasSize = re.compile("\{\{(I|Cosmetic)\|([^}]+)\|([\d]+)px\}\}")
                regexisBoring = re.compile("\[\[(.*?)\]\]")
                matchesNoSize = re.finditer(regexNoSize, line)
                matchesHasSize = re.finditer(regexHasSize, line)
                matchesisBoring = re.finditer(regexisBoring, line)

                for match in matchesHasSize:
                    template = match.group(1)
                    itemOriginal = match.group(2)
                    itemTranslation = getTranslatedStringV2(getEnglishTokenV2(itemOriginal), itemOriginal)
                    itemImage = match.group(3)
                    if itemTranslation:
                        text = text.replace(
                            "{{%s|%s|%spx}}" % (template, itemOriginal, itemImage),
                            "{{%s|%s|%spx}}" % (template, itemTranslation, itemImage)
                        )

                for match in matchesNoSize:
                    template = match.group(1)
                    itemOriginal = match.group(2)
                    itemTranslation = getTranslatedStringV2(getEnglishTokenV2(itemOriginal), itemOriginal)
                    if itemTranslation:
                        text = text.replace(
                            "{{%s|%s}}" % (template, itemOriginal),
                            "{{%s|%s}}" % (template, itemTranslation)
                        )

                for match in matchesisBoring:
                    itemOriginal = match.group(1)

                    exclude = [
                        "Ficheiro:",
                        "w:",
                        "en:",
                        "ru:",
                        "|",
                        "underlords:",
                        "zh:",
                        "Categoria:"
                    ]

                    if not any(ele in itemOriginal for ele in exclude) and itemOriginal[0].isupper():
                        itemTranslation = getTranslatedStringV2(getEnglishTokenV2(itemOriginal), itemOriginal)
                        if itemTranslation:
                            text = text.replace(
                                "[[%s]]" % (itemOriginal),
                                "[[%s]]" % (itemTranslation)
                            )

    # Todo: Use wikitextparser
    if "{{A|" in content or "{{Ability ID|" in content:
        for line in text.splitlines():
            if "{{A|" in line or "{{Ability ID|" in line:
                regexRequiredOnly = re.compile("\{\{(A|Ability ID)\|([^}]+)\|([^}]+)\}\}")
                matchesRequired = re.finditer(regexRequiredOnly, line)

                for match in matchesRequired:
                    template = match.group(1)
                    abilityOriginal = match.group(2)
                    abilityTranslation = getTranslatedStringV2(getEnglishTokenV2(abilityOriginal), abilityOriginal)
                    abilitySource = match.group(3)
                    text = text.replace(
                        "{{%s|%s|%s}}" % (template, abilityOriginal, abilitySource),
                        "{{%s|%s|%s}}" % (template, abilityTranslation, abilitySource)
                    )



    # Update infobox
    text = wtp.parse(text)

    for template in text.templates:
        if template.name.strip() == "Cosmetic Item infobox":
            for arg in template.arguments:
                if arg.name.strip() == "setname":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem1":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem2":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem3":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet
                
                if arg.name.strip() == "setitem4":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet
                
                if arg.name.strip() == "setitem5":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet
                
                if arg.name.strip() == "setitem6":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem7":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem8":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem9":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet

                if arg.name.strip() == "setitem10":
                    transSet = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transSet:
                        arg.value = " %s\n" % transSet
                
                if arg.name.strip() == "name":
                    transName = getTranslatedStringV2(getEnglishTokenV2(arg.value.strip()), arg.value.strip())
                    if transName:
                        arg.value = " %s\n" % transName

                if arg.name.strip() == "availability":
                    try:
                        links = wtp.parse(arg.value).wikilinks
                        newavail = []
                        if links:
                            for link in links:
                                transAvail = getTranslatedStringV2(getEnglishTokenV2(link.title), link.title)
                                if transAvail:
                                    newavail.append(" [[%s]]" % transAvail)
                            
                            arg.value = "%s\n" % ",".join(newavail)
                    except:
                        print("Availability falhou: " + arg.value)

    return str(text)

for page in gen:
    trans = getTranslatedStringV2(getEnglishTokenV2(page.title()), page.title())
    if trans:
        if page.title() != trans:
            print("\"%s\" será movido para \"%s\"" % (page.title(), trans))
            newtext = getTranslatedItems(page.text)
            page.text = u"" + newtext + ""
            page.save(u"Auto: Tradução preliminar para movimentação")
            print("Atualizando %s com nomes traduzidos." % page.title())
            redirecttarged = pywikibot.Page(site, trans)
            if redirecttarged.exists():
                print("Erro! O alvo do redirecionamento já existe: %s\n" % redirecttarged.title())
            else:
                print("Tudo limpo! Podemos mover a página.\n")
                page.move(trans, reason=u"Auto: Movendo página para nome localizado", movetalk=True, noredirect=False)
