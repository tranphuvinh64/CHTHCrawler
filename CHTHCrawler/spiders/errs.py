import scrapy
from scrapy.spiders import CrawlSpider
from .stores import Store

def getErrorLinks(link,strType):
    lst_links_store = []
    lst_links_page = []
    with open(link,"r") as f:
        for row in f:
            row = row.strip()
            lst = row.split("|")
            link = max(lst,key=len)
            if link.find("http") != -1:
                if link.find("page") != -1:
                    lst_links_page.append(link)
                else:
                    lst_links_store.append(link)
    if strType == "page":
        return lst_links_page
    if strType == "store":
        return lst_links_store
    return []
    

# class ErrorLinksStoreCrawler(scrapy.Spider):
#     name = 'errStore'
#     start_urls = getErrorLinks("./log/err.txt", "store")

#     def parse(self, response):
#         print("vinhdeptrai")
#         print(response.url)
#         Tinh = response.xpath('//ul[@class="pull-left breadcrumb"]/li[2]/a/span/text()').extract_first()
#         store = Store()
#         store.url = response.url
#         li = (response.xpath('//div[@class="article-content"]/span/ul/li'))
#         for i in range(1, len(li) + 1):
#             store.setAttribute(i, response=response)
#         store.toFile(response=response)
#         store.logging(response)