import os
import requests
import shutil
from bs4 import BeautifulSoup

if not os.path.exists("backpack"):
    os.makedirs("backpack")

warpaints = []

for warpaint in warpaints:
    print("Processando %s..." % warpaint)

    try:
        useragent = {
            "User-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.77 Safari/537.36 Vivaldi/1.7.735.27"
        }

        # Não é muito necessário já que agora as páginas são diferenciadas pelo desgaste
        try:
            url = "http://steamcommunity.com/market/listings/440/" + \
                warpaint.replace(" ", "%20") + \
                "%20War%20Paint%20%28Factory%20New%29"
            geturl = requests.get(url, headers=useragent)
            print("%s" % geturl.status_code)

        except:
            url = "http://steamcommunity.com/market/listings/440/" + \
                warpaint.replace(" ", "%20") + "%20War%20Paint"
            geturl = requests.get(url, headers=useragent)

        soup = BeautifulSoup(geturl.content, "html.parser")

        backpack = soup.find("div", attrs={"class": "market_listing_largeimage"}).find(
            "img")["src"].replace("360fx360f", "512fx512f")

        backpackimage = requests.get(backpack, headers=useragent, stream=True)

        with open("backpack/Backpack %s.png" % warpaint, "wb") as f:
            shutil.copyfileobj(backpackimage.raw, f)
            print("Imagem para %s salva!\n" % warpaint)

    except:
        print("A página para %s não foi encontrada!\n" % warpaint)
        with open("erros.txt", "a") as f:
            f.write("NÃO ENCONTRADO: \"" + warpaint + "\" em http://steamcommunity.com/market/listings/440/" +
                    warpaint.replace(" ", "%20") + "%20War%20Paint%20%28Factory%20New%29\n")
