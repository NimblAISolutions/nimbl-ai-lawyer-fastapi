from selenium.webdriver import Edge
from bs4 import BeautifulSoup as bs
from utils import log, Statuses
import json
from pprint import pprint

driver = Edge()

# Сезонность
seasons = [
    "sezonnost-is-all-season",
    "sezonnost-is-winter",
    "sezonnost-is-summer",
]

# Шины
types_of_tires = [
    "tyres",
    "lgruz",
    "gruz",
    "sh",
    "kgsh",
]

# Base link
# 1 param - type of tires
# 2 param - season
search_template = "https://aikos.kz/catalog/{tire}/search/{season}/?ajax_get=Y&ajax_get_filter=Y&PAGEN_1={page}"


def get_soup_from_url(url_: str):
    driver.get(url_)
    driver.delete_all_cookies()

    return bs(driver.page_source, "html.parser")


catalog_dict = {}
for type_of_tire in types_of_tires:
    catalog_dict[type_of_tire] = {}

    for season in seasons:
        catalog_dict[type_of_tire][season] = []
        page = 1

        # START BLOCK OF MAX_PAGE
        soup = get_soup_from_url(search_template.format(tire=type_of_tire, season=season, page=page))

        try:
            max_page = int(soup.find(
                "div", {"class": "module-pagination"}
            ).find_all(
                "a", {"class": "dark_link"}
            )[-1].text)
        except:
            max_page = 1
        # END BLOCK OF MAX_PAGE

        # гоняемся по пагинации пока наше число записей не настигнет 50
        while len(catalog_dict[type_of_tire][season]) <= 20:
            url = search_template.format(tire=type_of_tire, season=season, page=page)
            log(Statuses.INFO, url + " started")

            soup = get_soup_from_url(url)

            catalog = soup.find("div", {"class": "catalog_block items block_list"})
            if not catalog:
                log(Statuses.ERROR, url + " skipped (no catalog found)")
                break

            # пробег по каталогу
            for item in catalog.find_all("div", {"class": "item_block"}):
                img_src = item.find_next("img").get("src")
                link_tag = item.find_next("a", {"class": "dark_link"})
                name = link_tag.text

                count = int(item.find_next("span", {"class": "value"}).text.split(" ")[-1])
                price = int(item.find_next("span", {"class": "price_value"}).text.replace(" ", ""))

                catalog_dict[type_of_tire][season].append({
                    "image": "https://aikos.kz" + img_src,
                    "name": name,
                    "count": count,
                    "price": price,
                    "link": "https://aikos.kz" + link_tag.get("href"),
                })

            if page == max_page:
                break

            page += 1

        # После 50 записей (или меньше) мы ищем доп.инфу о них
        for idx, item in enumerate(catalog_dict[type_of_tire][season]):
            if item.get('link'):
                soup = get_soup_from_url(item.get('link'))
                characteristics = {}
                props = soup.find("div", {"class": "props props_list"}).find_all("div", {"class": "prop"})
                for prop in props:
                    name = prop.find_next("div", {"class": "name"}).text.replace("\n", "").replace("\t", "")
                    value = prop.find_next("div", {"class": "value"}).text.replace("\n", "").replace("\t", "")
                    characteristics[name] = value

                catalog_dict[type_of_tire][season][idx]["characteristics"] = characteristics


with open("aikos_tires.json", "w", encoding="utf-8") as outfile:
    json.dump(catalog_dict, outfile, ensure_ascii=False)
