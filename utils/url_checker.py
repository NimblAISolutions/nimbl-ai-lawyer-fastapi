import re
def url_checker(url):
    pattern = r"^(https?|ftp)://[^\s/$.?#].[^\s]*$"
    is_valid = re.match(pattern, url) is not None

    return is_valid