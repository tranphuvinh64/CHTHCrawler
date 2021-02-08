from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import re
from scrapy.exceptions import CloseSpider
from .config import firstpage, lastpage, firstpage_num, lastpage_num

def getStartURL_HCM():
    flag = 'https://www.cuahangtaphoa.com/danh-sach-cua-hang-tap-hoa-ho-chi-minh/'
    if os.path.isfile("./result/linkpage.txt"):
        with open("./result/linkpage.txt","r") as f:
            for line in f:
                if line.strip() != '':
                    flag = line.strip()
    return flag
                    
# if __name__ == "__main__":
#     print(getStartURL())

class HCMStoreSpider(CrawlSpider):
    name = 'hcm'
    start_urls = [firstpage]
    rules = (Rule(LinkExtractor(
                 restrict_xpaths='//p[@class="page-nav"]/a[text()="›"]'), callback='logging', follow=True),
             Rule(LinkExtractor(
                 restrict_xpaths='//div[@class="content_page"]/div[@class="news-v3 bg-color-white"]/div/h2/a'),
        callback='parse_item'),)
    


    def logging(self, response):
        active = response.xpath('//p[@class="page-nav"]/a[@class="page-nav-act active"]').extract_first()
        if response.url.find(lastpage) != -1 or active is None:
            raise CloseSpider("achieved limit page")
        with open("./result/linkpage.txt", "a+") as f:
            f.write(response.url)
            f.write("\n")

    def parse_item(self, response):
        store = Store()
        store.url = response.url
        li = (response.xpath('//div[@class="article-content"]/span/ul/li'))
        for i in range(1, len(li) + 1):
            store.setAttribute(i, response=response)
        store.toFile(response=response)
        


class ExceptHCMStoreSpider(CrawlSpider):
    name = 'exceptHCM'
    start_urls = [firstpage]
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//p[@class="page-nav"]/a[text()="›"]'), callback='loggingPage', follow=True),
        Rule(LinkExtractor(
                 restrict_xpaths='//div[@class="tc_have"]/ul/div[@class="news-v3 bg-color-white"]/div[not(div[@class="row"]/div[@class="col-md-4"]/p/a/strong[text()="Hồ Chí Minh"])]/h2/a'),
        callback='parse_item'),)
    def loggingPage(self, response):
        seperate = "|"
        active = response.xpath('//p[@class="page-nav"]/a[@class="page-nav-act active"]').extract_first()
        if response.url.find(lastpage) != -1 or active is None:
            with open(f"./log/{firstpage_num}_{lastpage_num}.txt", "a+") as f:
                f.write("done")
                f.write("\n")
            raise CloseSpider("achieved limit page")
        
        with open(f"./log/{firstpage_num}_{lastpage_num}.txt", "a+") as f:
            f.write(response.url)
            f.write(seperate)
            f.write(str(response.status))
            f.write("\n")

    def parse_item(self, response):
        Tinh = response.xpath('//ul[@class="pull-left breadcrumb"]/li[2]/a/span/text()').extract_first()
        store = Store()
        store.url = response.url
        li = (response.xpath('//div[@class="article-content"]/span/ul/li'))
        for i in range(1, len(li) + 1):
            store.setAttribute(i, response=response)
        store.toFile(response=response)
        store.logging(response)

class Store():
    def __init__(self) -> None:
        self.Tinh = "None"
        self.Huyen = "None"
        self.url = ""
        self.TenTiengAnh = ""
        self.MST = ""
        self.NganhNgheChinh = ""
        self.NgayCap = ""
        self.NgayHoatDong = ""
        self.DaiDienPhapLuat = ""
        self.DiaChi = ""
        self.NoiDangKy = ""
        self.ChuSoHuu = ""
        self.DienThoai = ""
        self.GoogleLink = ""
        self.seperate = "|"

    def setAttribute(self, index, response):
        strField = response.xpath(
            f'//div[@class="article-content"]/span/ul/li[{index}]/span/text()').extract_first()
        # print(f"strField {strField}")
        if strField == "Tên tiếng anh:":
            self.TenTiengAnh = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/text()').extract_first()
        if strField == "MST:":
            self.MST = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/b/span/text()').extract_first()
        if strField == "Ngành nghề chính:":
            self.NganhNgheChinh = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/text()').extract_first()
        if strField == "Ngày cấp:":
            self.NgayCap = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/text()').extract_first()
        if strField == "Ngày hoạt động:":
            temp1 = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/text()').extract_first()
            temp2 = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/i/text()').extract_first()
            if temp1 is not None and temp2 is not None:
                self.NgayHoatDong = temp1 + temp2
            else:
                self.NgayHoatDong = "None"
        if strField == "Đại diện pháp luật:":
            self.DaiDienPhapLuat = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/b/text()').extract_first()
        if strField == "Địa chỉ:":
            self.DiaChi = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/span[2]/text()').extract_first()
            self.GoogleLink = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/a/@href').extract_first()
        if strField == "Nơi đăng ký quản lý:":
            self.NoiDangKy = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/text()').extract_first()
        if strField == "Chủ sở hữu:":
            self.ChuSoHuu = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/b/text()').extract_first()
        if strField == "Điện thoại:":
            self.DienThoai = response.xpath(
                f'//div[@class="article-content"]/span/ul/li[{index}]/b/font/text()').extract_first()

    def toString(self):
        print(f"TenTiengAnh = {self.TenTiengAnh}")
        print(f"MST = {self.MST}")
        print(f"NganhNgheChinh = {self.NganhNgheChinh}")
        print(f"NgayCap = {self.NgayCap}")
        print(f"NgayHoatDong = {self.NgayHoatDong}")
        print(f"DaiDienPhapLuat = {self.DaiDienPhapLuat}")
        print(f"DiaChi = {self.DiaChi}")
        print(f"NoiDangKy = {self.NoiDangKy}")
        print(f"ChuSoHuu = {self.ChuSoHuu}")
        print(f"DienThoai = {self.DienThoai}")

    def toFile(self, response):
        self.Tinh = response.xpath(
            '//ul[@class="pull-left breadcrumb"]/li[2]/a/span/text()').extract_first()
        self.Huyen = response.xpath(
            '//ul[@class="pull-left breadcrumb"]/li[3]/a/span/text()').extract_first()
        self.Xa = response.xpath(
            '//ul[@class="pull-left breadcrumb"]/li[4]/a/span/text()').extract_first()
        with open("./result/"+"info_"+self.Tinh+".txt", 'a+') as f:
            f.write(response.url)
            f.write(self.seperate)
            if self.TenTiengAnh is None or self.TenTiengAnh.strip() == "":
                self.TenTiengAnh = "None"
            if self.MST is None or self.MST.strip() == "":
                self.MST = "None"
            if self.NganhNgheChinh is None or self.NganhNgheChinh.strip() == "":
                self.NganhNgheChinh = "None"
            if self.NgayCap is None or self.NgayCap.strip() == "":
                self.NgayCap = "None"
            if self.NgayHoatDong is None or self.NgayHoatDong.strip() == "":
                self.NgayHoatDong = "None"
            if self.DaiDienPhapLuat is None or self.DaiDienPhapLuat.strip() == "":
                self.DaiDienPhapLuat = "None"
            if self.DiaChi is None or self.DiaChi.strip() == "":
                self.DiaChi = "None"
            if self.NoiDangKy is None or self.NoiDangKy.strip() == "":
                self.NoiDangKy = "None"
            if self.ChuSoHuu is None or self.ChuSoHuu.strip() == "":
                self.ChuSoHuu = "None"
            if self.DienThoai is None or self.DienThoai.strip() == "":
                self.DienThoai = "None"
            if self.GoogleLink is None or self.GoogleLink.strip() == "":
                self.GoogleLink = "None"
            if self.Huyen is None or self.Huyen.strip() == "":
                self.Huyen = "None"
            if self.Xa is None or self.Xa.strip() == "":
                self.Xa = "None"
            f.write(self.TenTiengAnh.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.MST.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.NganhNgheChinh.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.NgayCap.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.NgayHoatDong.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.DaiDienPhapLuat.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.DiaChi.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.Tinh.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.Huyen.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.Xa.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.NoiDangKy.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.ChuSoHuu.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.DienThoai.replace("|", "/").replace("\n",""))
            f.write(self.seperate)

            f.write(self.GoogleLink.replace("|", "/").replace("\n",""))
            f.write("\n")

    def getResult(self):
        return [self.url,
                self.TenTiengAnh,
                self.MST,
                self.NganhNgheChinh,
                self.NgayCap,
                self.NgayHoatDong,
                self.DaiDienPhapLuat,
                self.DiaChi,
                self.NoiDangKy,
                self.ChuSoHuu,
                self.DienThoai]
    def logging(self, response):
        with open("./log/log_"+self.Tinh+".txt","a+") as f:
            f.write(response.url)
            f.write(self.seperate)
            f.write(str(response.status))
            f.write("\n")
