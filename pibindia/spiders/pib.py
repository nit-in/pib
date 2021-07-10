import scrapy
from scrapy_selenium import SeleniumRequest
from pathlib import Path
import requests
from datetime import datetime
import pdfkit
import re

# url = 'https://archive.pib.gov.in/archive2/erelease.aspx/'
url = "https://pib.gov.in/AllRelease.aspx"
pib_url = "https://pib.gov.in/PressReleaseIframePage.aspx?PRID="
cwd = Path.cwd()
chromedriver = "selenium/chromedriver"
chromedriver_path = Path(cwd, chromedriver).expanduser()


class PibSpider(scrapy.Spider):
    name = "pib"
    allowed_domains = ["pib.gov.in"]

    custom_settings = {
        "DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": str(chromedriver_path),
    }

    def start_requests(self):
        # self.rel_date = self.rel_date_fn()
        self.strp_date = datetime.strptime(self.rel_date, "%Y-%m-%d")
        self.rel_day = self.strp_date.strftime("%d")
        self.rel_month = self.strp_date.strftime("%m")
        self.rel_year = self.strp_date.strftime("%Y")
        self.pib_date = self.strp_date.strftime("%Y/%b/%d")
        self.jyr = f"document.forms.form1.ContentPlaceHolder1_ddlYear.value={str(self.rel_year).lstrip('0')};"
        self.jmin = f"document.forms.form1.ContentPlaceHolder1_ddlMinistry.value=0;"
        self.jday = f"document.forms.form1.ContentPlaceHolder1_ddlday.value={str(self.rel_day).lstrip('0')};"
        self.jmon = f"document.forms.form1.ContentPlaceHolder1_ddlMonth.value={str(self.rel_month).lstrip('0')};"
        self.submit = f"document.forms.form1.submit()"
        self.jsub = self.jmin + self.jday + self.jmon + self.jyr + self.submit
        yield SeleniumRequest(url=url, callback=self.parse_js, script=self.jsub)

    def parse_js(self, response):
        # for i in response.xpath("//div[contains(@class,'content-area')]/ul[contains(@class,'num')]"): #response.css("div.content-area ul.num"):
        # 	print(i.xpath("//h3").extract(),i.xpath("//li/a[contains(@href,'PRID')]").extract(),i.xpath("//h3/following-sibling").extract())
        for articles in response.xpath(
            "//div[contains(@class,'content-area')]/ul[contains(@class,'num')]/li/a[contains(@href,'PRID')]"
        ):
            pib_prid = str(articles.xpath("@href").get()).split("=", 1)[1]
            pib_title_un = (
                str(articles.xpath("@title").get())[:90]
                .replace(" ", "_")
                .replace("\n", "_")
            )
            pib_title_re = re.sub(
                "[`~!@#$%^&*();:',.+=<>|\\/?\n\t\r ]", "", pib_title_un
            )
            pib_title = pib_title_re + "_" + str(pib_prid) + ".pdf"
            pib_min_un = (
                str(articles.xpath("..//preceding-sibling::h3[1]/text()").get())
                .replace(" ", "_")
                .replace("&", "and")
                .replace("\n", "_")
            )
            pib_min = re.sub("[`~!@#$%^&*();:',.+=<>|\\/?\n\t\r ]", "", pib_min_un)
            pib_prlink = str(pib_url) + str(pib_prid)
            # print(self.pib_date,pib_min,pib_title,pib_prlink,sep="\n",end="\n\n\n")
            self.download_article(pib_title, pib_prlink, pib_min, self.pib_date)

    def download_article(self, art_title, art_link, art_min, art_date):
        pib_dir = "~/pib"
        pib_dir_path = Path(pib_dir).expanduser()
        if not pib_dir_path.exists():
            pib_dir_path.mkdir(parents=True)
        date_path = Path(pib_dir_path, art_date)
        min_path = Path(date_path, art_min)

        if not date_path.exists():
            date_path.mkdir(parents=True)
        if not min_path.exists():
            min_path.mkdir(parents=True)

        pdf_path = Path(min_path, art_title).expanduser()
        ops = {
            "quiet": "",
            "no-pdf-compression": "",
            "background": "",
            "page-size": "A4",
            "margin-top": "0.5in",
            "margin-right": "0.5in",
            "margin-bottom": "0.5in",
            "margin-left": "0.5in",
            "encoding": "UTF-8",
            "no-outline": None,
            "enable-javascript": "",
            "javascript-delay": "2000",
        }
        if pdf_path.exists():
            print(f"{pdf_path} already downloded.")
        else:
            print(f"downloading {pdf_path} ....")
            pdfkit.from_url(str(art_link), str(pdf_path), options=ops)
