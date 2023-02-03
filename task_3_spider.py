"""
Prerequisites

Install scrapy package using the command:

pip install scrapy

Run the spider using the follow command

scrapy runspider task_3_spider.py -o output.csv

Output is in form of CSV sheet named output.csv

Known issues that  can be improved:
- Description parsing for height and width can be improved with better regex
- Height and Width order is not maintained for cases where data is of form WxH
- Media field parsing is not 100% accurate
"""

import re

from scrapy import Spider, Request

class BearspaceSpider(Spider):
    name = "bearspace_spider"
    allowed_domains = ["bearspace.co.uk"]
    start_urls = ["https://www.bearspace.co.uk/purchase"]

    def parse(self, response):
        # Parse landing page
        page_num = response.meta.get("page_num", 1)
        product_links = response.css(
            "section[data-hook='product-list'] li[data-hook='product-list-grid-item'] a[data-hook='product-item-product-details-link']::attr(href)"
        ).getall()
        for link in product_links:
            yield Request(
                link,
                self.parse_product,
            )
        has_next_page = response.css("button[data-hook='load-more-button']")
        if has_next_page:
            next_page_num = page_num + 1
            yield Request(
                response.urljoin(f"purchase?page={next_page_num}"),
                self.parse,
                meta={"page_num": next_page_num}
            )

    def parse_product(self, response):
        title = response.css("h1[data-hook='product-title']::text").get()

        price_gbp = response.css("span[data-hook='formatted-primary-price']::text").get()
        clean_price = price_gbp.strip("£").replace(",", "")
        description = response.css("pre[data-hook='description'] *::text").getall()
        clean_description = [l.strip(" ").replace("\xa0", "") for l in description if l.strip(" ").replace("\xa0", "")]

        dim_capture = False
        dim_ix = None
        medium = None
        ht_value = None
        wt_value = None
        for ix, line in enumerate(description):
            if (("cm" in line) or ('x' in line) or ('X' in line)) and not dim_capture:
                dimension_txt = re.findall(r"(\d+\.?,?\d*)", line)
                # Known issue not all dimensions are captured in H x W format
                ht_value, wt_value, dt_value = dimension_txt + [None] * (3 - len(dimension_txt))
                if ht_value or wt_value:
                    dim_capture = True
                    dim_ix = ix
            if ix == 0 and not dim_capture and not "Artist:" in line:
                medium = line
            if not medium and dim_capture and ix == dim_ix + 1:
                medium = line


        yield(
            {
                "title": title,
                "price_gbp": clean_price,
                "url": response.url,
                "height_cm": ht_value,
                "width_cm": wt_value,
                "description": description,
                "media": medium
            }
        )
