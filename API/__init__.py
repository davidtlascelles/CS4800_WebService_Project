import json
import os
import time

import markdown

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
        return markdown.markdown(content)


@app.route('/result')
def result(score=None):
    return render_template('resultpage.html', score=score)


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
        return result(authenticity_score)
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
        "citation_urls": None
    }

    # CODE GOES HERE

    return page_data_dict


def authenticity_detector(json_deliverable):
    """
    Sends json object containing data to be screened in authenticity detector
    :param json_deliverable: json object
    :return: authenticity float score
    """
    result = 0.5
    time.sleep(3)
    print(json_deliverable)

    return result
