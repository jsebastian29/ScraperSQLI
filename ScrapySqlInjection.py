import urllib
import urllib.request
import re
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
import scrapy

class VulnerableSQLSitesCrawler(Spider):
    name = "SQLCrawler"

    def parse(self, response):
        urls_to_analyze = response.css(".kCrYT a").xpath("@href").getall()        

        for url in urls_to_analyze:
            url = re.search("url\\?q=(.+?)&", url)            

            if url is not None:
                full_url = urllib.request.unquote(url.groups(1)[0]) + "\'"
                yield scrapy.Request(full_url, meta={"download_timeout": 2, "dont_retry": True}, callback=self.check_vulnerability, errback=self.error_http)

    def check_vulnerability(self, response):
        body = response.css("body").get()
        if "You have an error in your SQL syntax" in body:
            self.create_vulnerable_urls_file(response.url)

    def create_vulnerable_urls_file(self, url):
        try:
            f = open("vulnerable_urls.txt", "a")
            f.write(url + "\n")
            f.close()
        except:
            print("Could not create file.")

    def error_http(self, failure):
        print("Bad HTTP response")
        
def start_google_spider(start_urls):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": 'INFO'
    })
    process.crawl(VulnerableSQLSitesCrawler, start_urls = start_urls)
    process.start()

def read_dorks(number_of_pages):
    try:
        start_urls = []
        google_url = "http://www.google.com/search"
        f = open("dorks.txt", "r")
        for dork in f.readlines():
            for page in range(0, int(number_of_pages)):
                payload = f"?q={dork}&start={page * 10}"
                complete_url = f"{google_url}{payload}"
                start_urls.append(complete_url)

        start_google_spider(start_urls)

        f.close()
    except Exception as e:
        print(e)
        print("Could not read file.")

if __name__ == "__main__":
    pages = input("Please provide the number of pages you want to analyze for each dork: ")
    read_dorks(pages)
    