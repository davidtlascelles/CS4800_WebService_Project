import json
import os
import time

import markdown
import requests
import pprint

# Import the framework
from flask import Flask
from flask import render_template, request, url_for, redirect
from flask_restful import Api

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


@app.route('/index')
def index():
    """HTML documentation about the API"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content, extensions=['tables'])


@app.route('/webapp')
def webapp():
    """"""


@app.route('/', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        url = request.form['url']
        page_data = web_scraper(url)
        attribute_dict = {
            'url': url,
            'post_data': {
                'account_name': request.form.get('post_author'),
                'user_name': request.form.get('user_name'),
                'post_date': request.form.get('post_date'),
                'post_date_time': request.form.get('post_date_time'),
                'account_age': request.form.get('account_age'),
                'profile_picture': request.form.get('profile_picture')
            },
            'page_data': page_data
        }
        authenticity_score = authenticity_detector(json.dumps(attribute_dict))
        return render_template('resultpage.html', score=authenticity_score)
    if request.method == 'GET':
        return render_template('submitpage.html')


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

    # Find page data json file and convert it to dictionary
    if page_html.find('application/ld+json') != -1:
        start = page_html.find("{", page_html.find('application/ld+json'))
        end = index_of_section_end(page_html, "{", "}", start)

    page_json = json.loads(page_html[start:end])

    #pprint.pprint(page_json)

    page_data_dict["title"] = find_title(page_json)
    page_data_dict["subtitle"] = find_subtitle(page_json)
    page_data_dict["authors"] = find_authors(page_json)
    page_data_dict["publisher"] = find_publisher(page_json)
    page_data_dict["publish_date"] = find_publish_date(page_json)
    page_data_dict["publish_date_time"] = find_publish_date_time(page_json)
    body_text, links = find_and_parse_body(page_html)
    page_data_dict["body"] = body_text
    page_data_dict["citation_urls"] = links
    #page_data_dict["html"] = page_html

    return page_data_dict


def find_title(data):
    title = None
    if "headline" in data:
        title = data["headline"]
    if "title" in data:
        title = data['title']

    return title


def find_subtitle(data):
    subtitle = None
    if 'description' in data:
        subtitle = data['description']
    if 'subtitle' in data:
        subtitle = data['subtitle']
    return subtitle


def find_authors(data):
    authors = None
    if 'by' in data:
        authors = data['by']
    if 'author' in data:
        authors = data['author']
    if 'authors' in data:
        authors = data['authors']
    if type(authors) is dict:
        authors = authors["name"]
    return authors


def find_publisher(data):
    publisher = None
    if 'publisher' in data:
        publisher = data['publisher']
    if type(publisher) is dict:
        publisher = publisher['name']
    return publisher


def find_publish_date(data):
    date = None
    if 'datePublished' in data:
        date = data['datePublished']
    if date.find("T") == -1:
        return date
    return None


def find_publish_date_time(data):
    date_time = None
    if 'datePublished' in data:
        date_time = data['datePublished']
    if date_time.find("T"):
        return date_time
    return None

def find_and_parse_body(html):

    if html.find('<p ') != -1:
        first_p = html.find("<p ")
        end_div = index_of_section_end(html, "<div", "</div", first_p)
        last_p = html.rfind("</p", 0, end_div) + 3
    body_section = html[first_p:last_p]
    paragraph_list = []
    links = []
    for index, letter in enumerate(body_section):
        if body_section[index:index+2] == "<p":
            start = index
        elif body_section[index:index+3] == "</p":
            p_line = body_section[start:index]
            p_start = p_line.find(">") + 1
            paragraph = p_line[p_start:index]
            if paragraph[len(paragraph) - 1] == ">":
                continue
            if paragraph.find("<") != -1:
                #text, link = find_links(paragraph)
                #links.append(link)
                #paragraph = text
                continue
            paragraph_list.append(paragraph)

    #for p in paragraph_list:
        #print(p)
    if len(links) == 0:
        links = None
    return paragraph_list, links


def index_of_section_end(html, start_str, end_str, start_index):
    last = start_index + 1
    open_count = 1
    while open_count > 0:
        start = html.find(start_str, last)
        close = html.find(end_str, last)
        if start != -1 and start < close:
            open_count += 1
            last = start + 1
        else:
            open_count -= 1
            last = close + 1
    return last


def find_links(text):
    new_text = ""
    print(text)
    start = 0
    end = 0
    while start != -1:
        start = text.find("<")
        new_text += text[end:start]
        end = index_of_section_end(text, "<", ">", start)
        text = text[end:]

    print(text[start:end])
    return None


def authenticity_detector(json_deliverable):
    """
    Sends json object containing data to be screened in authenticity detector
    :param json_deliverable: json object
    :return: authenticity float score
    """
    result = 0.5
    dict = json.loads(json_deliverable)
    pprint.pprint(dict)
    return result
