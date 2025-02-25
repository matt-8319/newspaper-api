#!/usr/bin/env python

from flask import Flask, url_for, request
from newspaper import Article
import os, json

app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/', methods = ['GET'])
@app.route('/topimage',methods = ['GET'])
def api_top_image():
    url = request.args.get('url')
    article = get_article(url)

    article = get_article_nlp(article)

    return json.dumps({
        "authors": article.authors,
        "html": article.html,
        "images:": list(article.images),
        "movies": article.movies,
        "publish_date": article.publish_date.strftime("%s") if article.publish_date else None,
        "text": article.text,
        "title": article.title,
        "topimage": article.top_image,
        "keywords": article.keywords,
        "summary": article.summary
    }), 200, {'Content-Type': 'application/json'}

def get_article_nlp(article):
    import nltk
    nltk.download('punkt')
    article.nlp()

    return article

def get_article(url):
    pdf_defaults = {"application/pdf": "%PDF-",
                    "application/x-pdf": "%PDF-",
                    "application/x-bzpdf": "%PDF-",
                    "application/x-gzpdf": "%PDF-"}
    article = Article(url, request_timeout=20, ignored_content_types_defaults=pdf_defaults)
    article.download()
    # uncomment this if 200 is desired in case of bad url
    # article.set_html(article.html if article.html else '<html></html>')
    article.parse()
    return article

if __name__ == '__main__':
    port = os.getenv('NEWSPAPER_PORT', '38765')
    app.run(port=int(port), host='0.0.0.0')
