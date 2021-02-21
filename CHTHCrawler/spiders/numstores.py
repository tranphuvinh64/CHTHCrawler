import scrapy

class NumStoreCrawler(scrapy.Spider):
    name = 'num'
    start_urls = ['https://www.cuahangtaphoa.com/']

    def parse(self, response):
        with open("numstore.txt","a+") as f:
            li = response.xpath("//ul[@class='collapse in']/li")
            for i in range(1, len(li) + 1):
                xpath_count = f"//ul[@class='collapse in']/li[{i}]/span/text()"
                xpath_province = f"//ul[@class='collapse in']/li[{i}]/a/text()"
                print("vinhdeptrai")
                province = response.xpath(xpath_province).extract_first()
                count = response.xpath(xpath_count).extract_first()
                count = count.replace(",","")
                f.write(province)
                f.write("|")
                f.write(count)
                f.write("\n")