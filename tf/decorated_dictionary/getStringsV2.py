from collections import OrderedDict
import os
import re

SCRIPTS_LOCATION = r"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Team Fortress 2\\tf\\resource"

tokenRE = re.compile(
    r'\"(?P<token>.[^\"]+)\"[\t\s]+\"(?P<transstring>.[^\"]+)\"[\n\r][\s\t]*\"\[english\](?P=token)\"[\t\s]+\"(?P<origstring>.[^\"]+)\"', re.DOTALL)
lineWithCaptionRE = re.compile(
    r'(\<.[^>]+\>){1,2}([\w\d\s]+:\s)?(?P<line>.+)', re.DOTALL)
escapeCharRE = re.compile(r"\||\*|''+|\[\[+|~")
dictionaryRE = re.compile(
    r'(?:^[ \t]*#[ \t]*([^\r\n]*?)[ \t]*$\s*)?^[ \t]*([^\r\n]+?[ \t]*(?:\|[ \t]*[^\r\n]+?[ \t]*)*):[ \t]*(?:[^\r\n]+?[ \t]*$|\s*[\r\n]+(?:\s*[ \t]+[-\w]+[ \t]*:[ \t]*[^\r\n]+[ \t]*$)+)', re.IGNORECASE | re.MULTILINE)

tf2_protodefs = {
    # "ar": "tf_proto_obj_defs_arabic.txt", // Invalid; No official support
    # Has dictionary support: https://wiki.tf/d/2097829
    "bg": "tf_proto_obj_defs_bulgarian.txt",
    "cs": "tf_proto_obj_defs_czech.txt",
    "da": "tf_proto_obj_defs_danish.txt",
    "de": "tf_proto_obj_defs_german.txt",
    "es": "tf_proto_obj_defs_spanish.txt",
    "fi": "tf_proto_obj_defs_finnish.txt",
    "fr": "tf_proto_obj_defs_french.txt",
    "hu": "tf_proto_obj_defs_hungarian.txt",
    "it": "tf_proto_obj_defs_italian.txt",
    # "ja": "tf_proto_obj_defs_japanese.txt", // File is not translated.
    "ko": "tf_proto_obj_defs_korean.txt",
    # "ka": "tf_proto_obj_defs_koreana.txt", // Copy of "ko"
    "nl": "tf_proto_obj_defs_dutch.txt",
    "no": "tf_proto_obj_defs_norwegian.txt",
    "pl": "tf_proto_obj_defs_polish.txt",
    "pt": "tf_proto_obj_defs_portuguese.txt",
    "pt-br": "tf_proto_obj_defs_brazilian.txt",
    "ro": "tf_proto_obj_defs_romanian.txt",
    "ru": "tf_proto_obj_defs_russian.txt",
    "sv": "tf_proto_obj_defs_swedish.txt",
    # Has dictionary support: https://wiki.tf/d/2097829
    "th": "tf_proto_obj_defs_thai.txt",
    "tr": "tf_proto_obj_defs_turkish.txt",
    # Has dictionary support: https://wiki.tf/d/2097829
    "uk": "tf_proto_obj_defs_ukrainian.txt",
    # "vi": "tf_proto_obj_defs_vietnamese.txt", // Has dictionary support: https://wiki.tf/d/2097829; File is not translated.
    "zh-hans": "tf_proto_obj_defs_schinese.txt",
    "zh-hant": "tf_proto_obj_defs_tchinese.txt"
}

decorated_collections = OrderedDict()
decorated_collections["Jungle Jackpot Collection"] = [
    "Anodized Aloha",
    "Bamboo Brushed",
    "Croc Dusted",
    "Leopard Printed",
    "Macaw Masked",
    "Mannana Peeled",
    "Park Pigmented",
    "Piña Polished",
    "Sax Waxed",
    "Tiger Buffed",
    "Yeti Coated"
]
decorated_collections["Infernal Reward War Paint Collection"] = [
    "Bank Rolled",
    "Bloom Buffed",
    "Bonk Varnished",
    "Cardboard Boxed",
    "Clover Camo'd",
    "Dream Piped",
    "Fire Glazed",
    "Freedom Wrapped",
    "Kill Covered",
    "Merc Stained",
    "Pizza Polished",
    "Quack Canvassed",
    "Star Crossed"
]
decorated_collections["Decorated War Hero Collection"] = sorted([
    "Carpet Bomber Mk.II",
    "Woodland Warrior Mk.II",
    "Wrapped Reviver Mk.II",
    "Forest Fire Mk.II",
    "Night Owl Mk.II",
    "Woodsy Widowmaker Mk.II",
    "Autumn Mk.II",
    "Plaid Potshotter Mk.II",
    "Civic Duty Mk.II",
    "Civil Servant Mk.II"
])
decorated_collections["Contract Campaigner Collection"] = sorted([
    "Dead Reckoner Mk.II",
    "Bovine Blazemaker Mk.II",
    "Backwoods Boomstick Mk.II",
    "Masked Mender Mk.II",
    "Macabre Web Mk.II",
    "Iron Wood Mk.II",
    "Nutcracker Mk.II",
    "Smalltown Bringdown Mk.II"
])
decorated_collections["Saxton Select Collection"] = ["Dragon Slayer"]
decorated_collections["Mann Co. Events Collection"] = ["Smissmas Sweater"]
decorated_collections["Winter 2017 Collection"] = sorted([
    "Miami Element",
    "Jazzy",
    "Mosaic",
    "Cosmic Calamity",
    "Hana",
    "Uranium",
    "Neo Tokyo",
    "Hazard Warning",
    "Damascus & Mahogany",
    "Dovetailed",
    "Alien Tech",
    "Cabin Fevered",
    "Polar Surprise",
    "Bomber Soul",
    "Geometrical Teams"
])
decorated_collections["Scream Fortress X Collection"] = sorted([
    "Electroshocked",
    "Tumor Toasted",
    "Ghost Town",
    "Skull Study",
    "Spectral Shimmered",
    "Calavera Canvas",
    "Spirit of Halloween",
    "Horror Holiday",
    "Totally Boned",
    "Haunted Ghosts"
])


def clean_string(string):
    res = lineWithCaptionRE.match(string)
    if res:
        clean_string = res.group("line").strip()
    else:
        clean_string = string.strip()

    return escape_string(clean_string)


def escape_string(string):
    if escapeCharRE.search(string):
        return "<nowiki>{0}</nowiki>".format(string)
    return string


# I have no idea what this does and I"m afraid I"ll never understand
trans_dict = OrderedDict()
for lang in tf2_protodefs:
    with open(SCRIPTS_LOCATION + os.sep + tf2_protodefs[lang], "r", encoding="utf-16") as f:
        content = f.read()
        matches = tokenRE.findall(content)

        for match in matches:
            token, transstring, origstring = match

            if token not in trans_dict:
                trans_dict[token] = {"en": origstring, lang: transstring}
            else:
                trans_dict[token][lang] = transstring

output = {}

for collection in decorated_collections:
    output[collection] = {}
    c_items_done = []

    for token in sorted(trans_dict.keys()):
        filename = tuple(token.split(".", 1))
        strings = trans_dict[token]
        string_en = strings["en"]

        if string_en in decorated_collections[collection]:
            if string_en not in c_items_done:
                c_items_done.append(string_en)

                dictionary_entry = "\n\n{filename}:".format(
                    collection=collection.lower(), filename=string_en.lower())

                dictionary_entry += "\n  en: {string}".format(
                    string=clean_string(string_en))

                langs = strings.keys()

                for lang in sorted(langs):
                    if lang is not "en":
                        dictionary_entry += "\n  {lang}: {string}".format(
                            lang=lang, string=clean_string(strings[lang]))

                output[collection][clean_string(string_en)] = dictionary_entry

with open("decorated_dictionary.txt", "w", encoding="utf-8") as f:
    for collection in decorated_collections:
        f.write("\n\n=== {0} ===\n\n<!--".format(collection))

        for item in decorated_collections[collection]:
            f.write(output[collection][item])

        f.write("\n\n-->")
