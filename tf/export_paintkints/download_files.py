# -------------------------------------------------- #
# Downloads item schema and gcfiles to local machine #
# -------------------------------------------------- #
from export_warpaints import export_warpaints
import importlib
import json

import requests
import os
import sys
import urllib.request

tf_dir = "C:\\program files (x86)\\steam\\steamapps\\common\\Team Fortress 2\\tf\\resource\\"
tf_proto = "tf_proto_obj_defs_english.txt"
tf_localization = "tf_english.txt"

gcfiles_date = "20181019"

if len(sys.argv) < 2:
    print("\nPlease input your Steam WebAPI key or use -download to start downloading.\n\nUsage:\n")
    print(
        "\t{script} steam_key\n\t{script} -download".format(script=sys.argv[0]))
    sys.exit(0)


steam_key = sys.argv[1]

url_schema = "http://api.steampowered.com/IEconItems_440/GetSchemaItems/v0001/?key={}&language=english".format(
    steam_key)
url_icons = "http://media.steampowered.com/apps/440/gcfiles_item_icons-{}.txt".format(
    gcfiles_date)

export_defindex = {}
export_paintkits = {}


def export_def_index():
    print("Exporting defindex...")

    with open("defindex.json", "w") as exported:
        json.dump(export_defindex, exported, indent=4, sort_keys=True)

    print("Exporting paintkit names...")
    export_paint_kits()


def export_paint_kits():
    with open(tf_dir + tf_proto, encoding="utf_16_le") as proto:
        content = proto.read()

        with open(tf_proto, "w", encoding="utf8") as proto_local:
            proto_local.write(content)

    with open(tf_proto, encoding="utf8") as proto:
        for line in proto:
            if line.strip().startswith("\"9_"):

                clean_line = line.strip()
                clean_id = clean_line.split("\"")[1].split("_")[1]
                clean_warpaint = clean_line.split("\"")[3]

                export_paintkits[clean_id] = clean_warpaint

    with open("paintkits.json", "w") as exported:
        json.dump(export_paintkits, exported, indent=4, sort_keys=True)


def download_schema(start=0, sround=1):
    response_schema = requests.get(
        url_schema + "&start={}".format(start), stream=True)

    with open("item_schema.json", "wb") as handle:
        print("Downloading item schema (round {})".format(sround))

        iterator = response_schema.iter_content()
        for data in iterator:
            handle.write(data)

    with open("item_schema.json", encoding="utf8") as schema:
        data = json.load(schema)

        for item in data["result"]["items"]:
            export_defindex[item["defindex"]] = item["item_name"]

        try:
            download_schema(data["result"]["next"], sround + 1)
        except:
            export_def_index()


def download_gc_icons():
    response_icons = requests.get(url_icons, stream=True)

    with open("gcfiles_item_icons.txt", "wb") as handle:
        iterator = response_icons.iter_content()

        for data in iterator:
            handle.write(data)


def remove_files():
    if os.path.exists(tf_proto):
        os.remove(tf_proto)

    if os.path.exists(tf_localization):
        os.remove(tf_localization)

    if os.path.exists("item_schema.json"):
        os.remove("item_schema.json")


if sys.argv[1] == "-download":
    print("Downloading paintkits...")
    export_warpaints()
else:
    print("Downloading item icons...")
    download_gc_icons()

    print("Downloading item schema...")
    download_schema()

    print("Cleaning up...")
    remove_files()

    export_warpaints()
