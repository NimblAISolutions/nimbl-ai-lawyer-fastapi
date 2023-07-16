from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.vectorstores import Milvus, Pinecone
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
from enum import Enum
from colorama import Fore, Style

driver = webdriver.Edge()


class Statuses(Enum):
    WARNING = Fore.RED
    SUCCESS = Fore.LIGHTGREEN_EX
    INFO = Fore.LIGHTYELLOW_EX
    ERROR = Fore.RED


# LOGGER HELPER FUNC
def log(status: Statuses, text: str):
    print(status.value + text + Style.RESET_ALL)


def parse_html(path: str, source: str):
    try:
        loader = UnstructuredHTMLLoader(
            path,
        )

        data = loader.load()
        # def processor(doc):
        #     doc.metadata["source"] = source
        #     return doc
        # docs = list(map(processor, docs))

    except Exception as e:
        return "Error: " + str(e)

    return ''.join([i.page_content for i in data])


def open_page_and_parse(url: str):
    driver.get(url)

    service, category, subcategory = url.split("/")[-3: ]
    BASE_PATH = os.path.join("parsed_data", service, category, subcategory)
    RAW_HTML_PATH = os.path.join(BASE_PATH, "raw.html")
    LINK_TXT_PATH = os.path.join(BASE_PATH, "link.txt")
    PARSED_TXT_PATH = os.path.join(BASE_PATH, "parsed.txt")

    isExist = os.path.exists(f"./{BASE_PATH}")
   
    if not isExist:
        os.makedirs(f"./{BASE_PATH}")

    content_bs = bs(driver.page_source, 'html.parser').find('div', {"class": "content"})
    for unsued_element in content_bs.find_all(attrs={"class": "hidden-print"}):
        unsued_element.decompose()


    with open(LINK_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(url)

    with open(RAW_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(str(content_bs))
    parsed_html = parse_html(RAW_HTML_PATH, url)
    
    with open(PARSED_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(str(parsed_html))
        
    return parsed_html


def parser_wrapper(path: str):
    try:
        documents = open_page_and_parse(path)
        if len(documents) < 1:
            log(Statuses.ERROR, path + " No content!")

        log(Statuses.SUCCESS, path + " loaded")

    except Exception as e:
        log(Statuses.ERROR, str(e))


def extract_links_from_a(tag, egov_url = "https://egov.kz"):
    links = []
    for link in tag.find_all('a', {"rel": "noopener noreferrer"}):
        links.append(egov_url + link['href'])
    return links


# Parser for https://egov.kz/cms/ru
def load_from_home_page():
    driver.get("https://egov.kz/cms/ru")
    html_categories = bs(driver.page_source).find("ul", {"class": "subcategories-list-new"})
    links = extract_links_from_a(html_categories)

    for link in links:
        driver.get(link)
        html_bs = bs(driver.page_source, 'html.parser')
        category_links = extract_links_from_a(html_bs.find("ul", {"class": "egov-submenu"}))
        for category_link in category_links:
            driver.get(category_link)
            html_category_bs = bs(driver.page_source, 'html.parser')
            try:
                useful_info_links = extract_links_from_a(html_category_bs.find_all("div", {"class": "block-horizontal items-list"})[-1])
                for useful_info_link in useful_info_links:
                    parser_wrapper(useful_info_link)
            except:
                continue


# Parser for https://egov.kz/cms/ru/online-services/for_citizen (all services)
def services_list_parser():
    driver.get('https://egov.kz/cms/ru/online-services/for_citizen')
    egov_url = "https://egov.kz"
    html_source = bs(driver.page_source, "html.parser")
    categories = html_source.find_all('div', {"class": 'category-item'})
    links = []
    for category in categories:
        links.append(*extract_links_from_a(category, egov_url))


    for link in links:
        parser_wrapper(link)    


def main():

    services_list_parser()

    # List of urls for Unstructed parse
    # urls = [
    #     "https://egov.kz/cms/ru/online-services/for_citizen/pass_sr18"
    # ]
    # Engine for list of urls
    # for url in urls:
    #     log(Statuses.INFO, url + " parsing...")
    #     parser_wrapper(url)
    #     log(Statuses.INFO, url + " parsed!")
    #     print()

    driver.close()
    log(Statuses.SUCCESS, "+="*3 + "FINISH" + "=+"*3)


load_from_home_page()
