from plugins.base import BaseProvider
import cloudscraper
from bs4 import BeautifulSoup
from pprint import pprint



class SilentQuill(BaseProvider):

    name = "SilentQuill"
    baseUrl = "https://www.silentquill.net/"

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.request_timeout = 15



    def fetch_home(self):
        #title
        #cover
        #link
        r = self.scraper.get(self.baseUrl)
        soup = BeautifulSoup(r.text, "html.parser")
        seldata = soup.select(".limit > img")
        selLink = soup.select(".bsx > a")

        results = []

        for i in range(0,19):
            title = seldata[i]["title"]
            cover = seldata[i]["data-src"].lstrip('/')
            link  = selLink[i]["href"].lstrip('/')
        
            results.append({
                "title": title,
                "cover": cover,
                "link": link

            })

    


        return results

    def get_details(self, url):
        r = self.scraper.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        desc_tag = soup.select_one("#kdt8-syn p")
        desc = desc_tag.get_text(strip=True) if desc_tag else ""

        items = soup.select(".eplister ul li")
        print(f"capitulos encontrados: {len(items)}")

        

        chapters      = []
        chaptersLinks = []

        for item in items:
            num  = item.get("data-num", "")
            link = item.select_one("a")
            if link:
                chapters.append(f"Chapter {num}")
                chaptersLinks.append(link["href"])



        

        return [{
            "desc": desc,
            "author": "",
            "chapters": chapters,
            "chaptersLinks": chaptersLinks
        }]

    def search_mango(self, name):
        #tittle
        #cover
        #link
        #https://www.silentquill.net/?s=ore+no
        slugName = name.replace(" ", "+")
        url = f"https://www.silentquill.net/?s={slugName}"
        r = self.scraper.get(url)
        soup = BeautifulSoup(r.text, "html")
        seldata = soup.select(".limit > img")
        selLink = soup.select(".bsx > a")
        items = soup.select(".bs")

        results = []


        title = [item["title"] for item in seldata]
        cover = [item["data-src"].lstrip('/') for item in seldata]
        link =  [item["href"].lstrip('/') for item in selLink]

    
        
        for index, t in enumerate(title):
            results.append({
                "title": t,
                "cover": cover[index],
                "link": link[index]
            })




        return results

    def get_pages(self, chapter_url):
        #pageList
        #chapter
        #name


        raise NotImplementedError