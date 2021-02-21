from scrapy.spiders import CrawlSpider, Rule
from .config import firstpage_link,firstpage_link_num,lastpage_link,lastpage_link_num
from scrapy.linkextractors import LinkExtractor
import pytz
from datetime import datetime
import re

class LinksCrawler(CrawlSpider):
    name = 'links'
    start_urls = [firstpage_link]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//p[@class="page-nav"]/a[text()="›"]'), 
            callback='getLinks', follow=True, errback='logError'),)
    def getLinks(self, response):
        pagenum = re.findall(r"page-[0-9]+",response.url)[0]
        formattime = "%Y:%m:%d %H:%M:%S"
        timezone = 'Asia/Saigon'
        str_currenttime = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone)).strftime(formattime)
        xpath_links = "//div[@class='news-v3 bg-color-white']/div/h2/a/@href"
        xpath_provinces = "//div[@class='news-v3 bg-color-white']/div/div[1]/div[2]/p/a/strong/text()"
        links = response.xpath(xpath_links).extract()
        provinces = response.xpath(xpath_provinces).extract()
        if len(links) == len(provinces):
            for i in range(len(links)):
                with open("links.txt","a+") as f:
                    f.write(str_currenttime)
                    f.write("|")
                    f.write(pagenum)
                    f.write("|")
                    f.write(links[i])
                    f.write("|")
                    f.write(provinces[i])
                    f.write("\n")
                
