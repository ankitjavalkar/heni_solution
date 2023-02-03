"""
Pre-requisites

Run the following commands to install the required dependencies

pip install lxml
pip install pandas
pip install requests

Usage

Run the script using the command:

python task_1_parsing_html.py
"""

from lxml import html
import re
import requests
import pandas as pd
from datetime import datetime

#get html and tree
html_page_link = 'candidateEvalData/webpage.html'
with open(html_page_link) as f:
    doc = f.read()

htmltree = html.fromstring(doc)

# parse artist name
aname_sel = htmltree.xpath("//h1[@id='main_center_0_lblLotPrimaryTitle']/text()")
artist_name = None
if aname_sel:
    name_txt = aname_sel[0]
    if '(b.' in name_txt:
        artist_name = name_txt.split('(b')[0]
    else:
        artist_name = name_txt

#parse painting name
pname_sel = htmltree.xpath("//h2[@id='main_center_0_lblLotSecondaryTitle']/i/text()")
painting_name = None
if pname_sel:
    pname_txt = pname_sel[0]
    painting_name = pname_txt.strip()

#parse price GBP
gbp_price_sel = htmltree.xpath("//span[@id='main_center_0_lblPriceRealizedPrimary']/text()")
clean_gbp_price = None
if gbp_price_sel:
    gbp_raw_txt = gbp_price_sel[0]
    gbp_unit, gbp_price_txt = gbp_raw_txt.split(' ')
    clean_gbp_price = int(gbp_price_txt.replace(',', ''))

#parse price US
usd_price_sel = htmltree.xpath("//span[@id='main_center_0_lblPriceRealizedPrimary']/text()")
clean_usd_price = None
if usd_price_sel:
    usd_raw_txt = gbp_price_sel[0]
    usd_unit, usd_price_txt = usd_raw_txt.split(' ')
    clean_usd_price = int(usd_price_txt.replace(',', ''))

#parse price GBP est
gbp_estimate_sel = htmltree.xpath("//span[@id='main_center_0_lblPriceEstimatedPrimary']/text()")
clean_gbp_est = None
if gbp_estimate_sel:
    gbp_est_raw_txt = gbp_estimate_sel[0]
    gbp_price_low_lim_txt, gbp_price_up_lim_txt = re.findall("([0-9,.]+)", gbp_est_raw_txt)
    clean_gbp_price_low_lim = int(gbp_price_low_lim_txt.replace(',', ''))
    clean_gbp_price_up_lim = int(gbp_price_up_lim_txt.replace(',', ''))
    clean_gbp_est = [clean_gbp_price_low_lim, clean_gbp_price_up_lim]

#parse price US est
usd_estimate_sel = htmltree.xpath("//span[@id='main_center_0_lblPriceEstimatedSecondary']/text()")
clean_usd_est = None
if usd_estimate_sel:
    usd_est_raw_txt = usd_estimate_sel[0]
    usd_price_low_lim_txt, usd_price_up_lim_txt = re.findall("([0-9,.]+)", usd_est_raw_txt)
    clean_usd_price_low_lim = int(usd_price_low_lim_txt.replace(',', ''))
    clean_usd_price_up_lim = int(usd_price_up_lim_txt.replace(',', ''))
    clean_usd_est = [clean_usd_price_low_lim, clean_usd_price_up_lim]

#image link
img_link_sel = htmltree.xpath("//img[@id='imgLotImage']/@src")
img_link = None
if img_link_sel:
    img_link = img_link_sel[0]

# sale date
sale_date_sel = htmltree.xpath("//span[@id='main_center_0_lblSaleDate']/text()")
sale_date = None
if sale_date_sel:
    sale_date_raw_txt = sale_date_sel[0].strip(', ')
    dt_obj = datetime.strptime(sale_date_raw_txt, '%d %B %Y')
    sale_date = datetime.strftime(dt_obj, '%Y-%m-%d')

df = pd.DataFrame()
df["artist_name"] = artist_name,
df["painting_name"] = painting_name,
df["realised_price_gbp"] = clean_gbp_price,
df["realised_price_usd"] = clean_usd_price,
df["estimate_in_gbp"] = clean_gbp_est,
df["estimate_in_usd"] = clean_usd_est,
df["image_url"] = img_link,
df["sale_date"] = sale_date,

print(df)

