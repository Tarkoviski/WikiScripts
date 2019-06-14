import json
import os
import re
import requests
import shutil
import time


def export_warpaints():
    base_url = "http://media.steampowered.com/apps/440/"

    if not os.path.exists("icons"):
        os.mkdir("icons")

    if not os.path.exists("icons_festive"):
        os.mkdir("icons_festive")

    wears = {
        "1": "Factory New",
        "2": "Minimal Wear",
        "3": "Field-Tested",
        "4": "Well-Worn",
        "5": "Battle Scarred"
    }

    item_names = {}

    with open("defindex.json") as index:
        item_names = json.load(index)

    paint_kits = {}

    with open("paintkits.json") as paintkits:
        paint_kits = json.load(paintkits)

    with open("gcfiles_item_icons.txt") as icons:
        for line in icons:
            if line.startswith("icons/generated_paintkit_icons/paintkit"):
                success = False
                while (not success):
                    try:
                        warpaint = re.search(
                            r"icons/generated_paintkit_icons/paintkit(\d+)_item(\d+)_wear(\d+)(_festive)?", line)

                        if warpaint == None or (warpaint.group(1) == "0" and warpaint.group(2) == "15013"):
                            success = True
                            continue

                        warpaint_id = warpaint.group(1)
                        warpaint_item = warpaint.group(2)
                        warpaint_wear = warpaint.group(3)
                        warpaint_festive = warpaint.group(4)

                        fileurl = base_url + line

                        filename_festive = "Backpack Festivized {} {} {}.png".format(paint_kits[warpaint_id],
                                                                                     item_names[warpaint_item], wears[warpaint_wear])
                        filename = "Backpack {} {} {}.png".format(paint_kits[warpaint_id],
                                                                  item_names[warpaint_item], wears[warpaint_wear])

                        headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
                                   'Accept': '*/*',
                                   'Connection': 'keep-alive',
                                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'}

                        if not os.path.exists("icons_festive/" + filename_festive) or not os.path.exists("icons/" + filename):
                            with requests.get(fileurl.strip(), headers=headers) as response:
                                print(response)

                                if warpaint_festive:
                                    with open("icons_festive/" + filename_festive, "wb") as bp:
                                        bp.write(response.content)
                                else:
                                    with open("icons/" + filename, "wb") as bp:
                                        bp.write(response.content)
                        else:
                            print("Ignoring downloaded file")

                        success = True
                    except requests.HTTPError:
                        # To do: how the hell do you get information from the HTTPError object in python
                        print("HTTP Error downloading {}".format(line))
                    except requests.Timeout:
                        print("Timed out while downloading {}".format(line))
                    finally:
                        time.sleep(.5)
