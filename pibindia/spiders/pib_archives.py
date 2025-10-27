import scrapy
from pathlib import Path
import requests
from datetime import datetime
import platform
from scrapy import FormRequest
import pibindia.spiders.config as config
from pibindia.modules.utils import *
from pibindia.modules.date_handler import *
from pibindia.modules.file_handler import *
from pibindia.modules.json_handler import *
from pibindia.modules.downloader import *

# url = 'https://archive.pib.gov.in/archive2/erelease.aspx/'
url = "https://archive.pib.gov.in/archive2/erelease.aspx"
pib_url = "https://archive.pib.gov.in/newsite/PrintRelease.aspx?relid="
cwd = Path.cwd()
platform_release = str(platform.release())
today = datetime.today()
pib_json_data = []


class PibSpider(scrapy.Spider):
    name = "pib_archives"
    start_urls = ["https://archive.pib.gov.in/archive2/erelease.aspx"]

    def parse(self, response):
        # self.rel_date = self.rel_date_fn()
        self.strp_date = datetime.strptime(self.rel_date, "%Y-%m-%d")
        self.minis_code = self.rel_mincode

        if (
            self.strp_date.date() == today.date()
            and "azure" in platform_release.lower()
        ) or (self.strp_date.date() > today.date()):
            print(f"Skipping as {self.strp_date.date()} is greater than {today.date()}")
            pass
        else:
            self.rel_day = dd(self.rel_date)
            self.rel_month = mm(self.rel_date)
            self.rel_year = yyyy(self.rel_date)
            self.pib_date = yyyymmmdd(self.rel_date)
            self.one = "1|"
            self.jyr = f"{str(self.rel_year).lstrip('0')}|"
            self.jmin = f"{str(self.minis_code)}"
            self.jday = f"{str(self.rel_day).lstrip('0')}|"
            self.jmon = f"{str(self.rel_month).lstrip('0')}|"
            self.jsub = self.one + self.jday + self.jmon + self.jyr + self.jmin
            pib_data = {"__CALLBACKID": "__Page", "__CALLBACKPARAM": str(self.jsub)}
            yield FormRequest.from_response(
                response, formdata=pib_data, callback=self.parse_asp
            )

    def parse_asp(self, response):
        # for i in response.xpath("//div[contains(@class,'content-area')]/ul[contains(@class,'num')]"): #response.css("div.content-area ul.num"):
        # 	print(i.xpath("//h3").extract(),i.xpath("//li/a[contains(@href,'PRID')]").extract(),i.xpath("//h3/following-sibling").extract())
        for articles in response.xpath("//li[contains(@onclick,'Getrelease')]"):
            pib_prid = str(articles.xpath("@id").get())
            pib_title_unnorm = str(articles.xpath("text()").get())[:90]
            pib_title_norm = remove_html_entities(pib_title_unnorm)

            pib_title_re = sanitize_name(pib_title_norm)
            pib_title = pib_title_re + "_" + str(pib_prid) + ".pdf"

            pib_min_unnorm = str(
                articles.xpath("..//preceding-sibling::li[1]/text()").get()
            )
            pib_min_norm = remove_html_entities(pib_min_unnorm)
            pib_min = sanitize_name(pib_min_norm)

            pib_prlink = str(pib_url) + str(pib_prid)
            jdate = ddmmmyyyy(self.rel_date)
            pib_json_data.append(
                article_jdata(
                    pib_prid, jdate, pib_title_unnorm, pib_min_unnorm, pib_prlink
                )
            )
            #            print(self.pib_date, pib_min, pib_title, pib_prlink, sep="\n", end="\n\n\n")
            self.download_article(pib_title, pib_prlink, pib_min, self.pib_date)

    def download_article(self, art_title, art_link, art_min, art_date):
        pib_dir = config.PIB_BASE_DIR
        pib_art_dir = config.PIB_ARTICLES_DIR
        pib_links = config.PIB_LINKS_DIR
        pib_json = config.PIB_JSON_DIR

        check_make_dir(pib_dir)
        check_make_dir(pib_art_dir)
        check_make_dir(pib_links)
        check_make_dir(pib_json)

        date_path = make_file_path(pib_art_dir, art_date)
        min_path = make_file_path(date_path, art_min)

        check_make_dir(date_path)
        check_make_dir(min_path)

        tnj_date = dd_mmm_yyyy(art_date)
        textf_name = "PIB_LINKS_" + str(tnj_date) + ".txt"
        textf_path = make_file_path(pib_links, str(textf_name))

        touch_file(textf_path)
        edit_file(textf_path, art_link)
        # json
        jfname = "PIB_JSON_" + str(tnj_date) + ".json"
        jfpath = make_file_path(pib_json, jfname)
        delete_file(jfpath)
        save_json(jfpath, pib_json_data)

        pdf_path = make_file_path(min_path, art_title)
        download_article(pdf_path, art_link)
