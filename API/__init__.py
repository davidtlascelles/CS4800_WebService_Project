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
        json_object = web_scraper(url)
        authenticity_score = authenticity_detector(json_object)
        return result(authenticity_score)
    if request.method == 'GET':
        return render_template('submitpage.html')


def web_scraper(url):
    """
    Scrapes a webpage for necessary components for detection services
    :param url: URL for webpage to be scraped
    :return: JSON of components that have been scraped
    """
    json_deliverable = {
        "url": url,
        "title": None,
        "authors": None,
        "publish date": None,
    }

    # CODE GOES HERE

    return json.dumps(json_deliverable)


def authenticity_detector(json_package):
    """
    Sends json object containing data to be screened in authenticity detector
    :param json_package: json object
    :return: authenticity float score
    """
    result = 0.5
    time.sleep(3)
    print(json_package)

    return result
