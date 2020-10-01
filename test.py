import requests
import pprint

def web_scraper(url):
    """
    Scrapes a webpage for necessary components for detection services
    :param url: URL for webpage to be scraped
    :return: JSON of components that have been scraped
    """
    page_data_dict = {
        "title": None,
        "subtitle": None,
        "authors": None,
        "publisher": None,
        "publish_date": None,
        "publish_date_time": None,
        "body": None,
        "citation_urls": None,
        "html": None
    }

    page_html = requests.get(url).content.decode().strip()
    for index, line in enumerate(page_html.splitlines()):
        if line.find("author") != -1:
            print(index, ":", line)


    page_data_dict["html"] = page_html

    return page_data_dict


url = "https://abcnews.go.com/Politics/wireStory/facebook-twitter-flounder-qanon-crackdown-73370661?cid=clicksource_4380645_4_heads_hero_live_headlines_hed"
web_scraper(url)
