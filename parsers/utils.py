from enum import Enum
from colorama import Fore, Style


class Statuses(Enum):
    WARNING = Fore.RED
    SUCCESS = Fore.LIGHTGREEN_EX
    INFO = Fore.LIGHTYELLOW_EX
    ERROR = Fore.RED


# LOGGER HELPER FUNC
def log(status: Statuses, text: str):
    print(status.value + text + Style.RESET_ALL)


# Useful tool to extract all links within object
def extract_links_from_tag(tag, base_url=""):
    links = []
    for link in tag.find_all('a', href=True):
        links.append(base_url + link.get("href"))
    return links
