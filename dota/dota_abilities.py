import re
import pywikibot
from pywikibot import pagegenerators

site = pywikibot.Site()

categories = [
    "Categoria:Heróis",
    "Categoria:Versões_do_jogo",
    "Categoria:Atualizações"
]

for category in categories:
    cat = pywikibot.Category(site, category)
    gen = pagegenerators.CategorizedPageGenerator(cat)

    def getEnglishTokenV2(string):
        with open("abilities_english.txt", encoding="utf16") as abilities_english:
            for line in abilities_english:
                line = line.rstrip()

                if string in line:
                    regex = re.compile("\"(.[^\"]+)\"[\t\s]+\"(.[^\"]+)\"")
                    matches = re.finditer(regex, line)

                    for match in matches:
                        if match and match.group(2) == string:
                            if "DOTA_Tooltip_ability_" in match.group(1):
                                return match.group(1)
                            else:
                                break
        abilities_english.close()

    def getTranslatedStringV2(token, original):
        with open("abilities_brazilian.txt", encoding="utf16") as translated_abilities:
            for line in translated_abilities:
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

        translated_abilities.close()

    for page in gen:
        if "{{A|" in page.text or "{{Ability ID|" in page.text:
            textOld = page.text
            text = page.text

            for line in text.splitlines():
                if "{{A|" in line or "{{Ability ID|" in line:
                    regexRequiredOnly = re.compile(
                        "\{\{(A|Ability ID)\|([^}]+)\|([^}]+)\}\}")
                    matchesRequired = re.finditer(regexRequiredOnly, line)

                    for match in matchesRequired:
                        template = match.group(1)
                        abilityOriginal = match.group(2)

                        abilityTranslation = getTranslatedStringV2(
                            getEnglishTokenV2(abilityOriginal), abilityOriginal)

                        abilitySource = match.group(3)

                        text = text.replace(
                            "{{%s|%s|%s}}" % (
                                template, abilityOriginal, abilitySource),
                            "{{%s|%s|%s}}" % (
                                template, abilityTranslation, abilitySource)
                        )

            if textOld == text:
                print("Não atualizando %s porque não temos nomes." % page)
            else:
                page.text = u"" + text + ""
                page.save(u"Auto: Tradução automática de nomes de habilidades")

                print("Atualizando %s com nomes traduzidos." % page)
