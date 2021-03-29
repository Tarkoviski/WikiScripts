import re
import pywikibot
from pywikibot import pagegenerators
import wikitextparser as wtp

site = pywikibot.Site()
siteEn = pywikibot.Site("en", "dota2")

heroes = [
    "Abaddon",
    "Alchemist",
    "Axe",
    "Beastmaster",
    "Brewmaster",
    "Bristleback",
    "Centaur Warrunner",
    "Chaos Knight",
    "Clockwerk",
    "Doom",
    "Dragon Knight",
    "Earth Spirit",
    "Earthshaker",
    "Elder Titan",
    "Huskar",
    "Io",
    "Kunkka",
    "Legion Commander",
    "Lifestealer",
    "Lycan",
    "Magnus",
    "Night Stalker",
    "Omniknight",
    "Phoenix",
    "Pudge",
    "Sand King",
    "Slardar",
    "Snapfire",
    "Spirit Breaker",
    "Sven",
    "Tidehunter",
    "Timbersaw",
    "Tiny",
    "Treant Protector",
    "Tusk",
    "Underlord",
    "Undying",
    "Wraith King",
    "Anti-Mage",
    "Arc Warden",
    "Bloodseeker",
    "Bounty Hunter",
    "Broodmother",
    "Clinkz",
    "Drow Ranger",
    "Ember Spirit",
    "Faceless Void",
    "Gyrocopter",
    "Hoodwink",
    "Juggernaut",
    "Lone Druid",
    "Luna",
    "Medusa",
    "Meepo",
    "Mirana",
    "Monkey King",
    "Morphling",
    "Naga Siren",
    "Nyx Assassin",
    "Phantom Assassin",
    "Phantom Lancer",
    "Razor",
    "Riki",
    "Shadow Fiend",
    "Slark",
    "Sniper",
    "Spectre",
    "Templar Assassin",
    "Terrorblade",
    "Troll Warlord",
    "Ursa",
    "Vengeful Spirit",
    "Venomancer",
    "Viper",
    "Weaver",
    "Ancient Apparition",
    "Bane",
    "Batrider",
    "Chen",
    "Crystal Maiden",
    "Dark Seer",
    "Dark Willow",
    "Dazzle",
    "Death Prophet",
    "Disruptor",
    "Enchantress",
    "Enigma",
    "Invoker",
    "Jakiro",
    "Keeper of the Light",
    "Leshrac",
    "Lich",
    "Lina",
    "Lion",
    "Nature's Prophet",
    "Necrophos",
    "Ogre Magi",
    "Oracle",
    "Outworld Devourer",
    "Puck",
    "Pugna",
    "Queen of Pain",
    "Rubick",
    "Shadow Demon",
    "Shadow Shaman",
    "Silencer",
    "Skywrath Mage",
    "Storm Spirit",
    "Techies",
    "Tinker",
    "Visage",
    "Void Spirit",
    "Warlock",
    "Windranger",
    "Winter Wyvern",
    "Witch Doctor",
    "Zeus",
    "Mars"
]

heroesBrazil = {"Mars": "Marte"}

for hero in heroes:
    heroEn = hero
    if hero in heroesBrazil.keys():
        hero = heroesBrazil[hero]

    heroEnglish = pywikibot.Page(siteEn, heroEn)
    heroBrazilian = pywikibot.Page(site, hero)
    heroEnglishParsed = wtp.parse(heroEnglish.text)
    heroBrazilianParsed = wtp.parse(heroBrazilian.text)
    heroBrazilianParsedNew = heroBrazilianParsed
    templateToCheck = "Hero infobox"
    for template in heroEnglishParsed.templates:
        if template.name.strip() == templateToCheck:
            for templateBrazil in heroBrazilianParsedNew.templates:
                if templateBrazil.name.strip() == templateToCheck:
                    for argBrazil in templateBrazil.arguments:
                        if template.get_arg(argBrazil.name):
                            templateBrazil.set_arg(
                                argBrazil.name,
                                template.get_arg(argBrazil.name).value.replace(
                                    "File:", "Ficheiro:"
                                ),
                                preserve_spacing=False,
                            )

    heroBrazilian.text = u"" + str(heroBrazilianParsedNew) + ""
    heroBrazilian.save(u"Auto: Atualização da Hero infobox")
