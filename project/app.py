#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from flask import Flask
from flask import g, render_template, url_for, redirect, abort, request
from datetime import date, datetime
import re
from unicodedata import normalize

app = Flask(__name__)
app.debug = True

page = {
    'title': '',
    'title_fb': '',
    'url': '',
    'description': '',
    'description_fb': '',
    'twitter': '',
    'author': '"Interactive Project", "Kelli R. Parker", "Joe Murphy"',
    'datestamp': '2017-08-02',
    'keywords': '',
    'keywords_array': '',
    'shareimg': '',
    'shareimg_static': '',
    'shareimgdesc': '',
}

with app.app_context():
    app.url_root = '/'
    app.page = page
    app.sitename = ''


class JsonQuery(object):
    ''' Methods for handling and querying the json data.
        '''
    def __init__(self, data):
        self.data = data

    def get_uniques(self, field):
        ''' Given a field, get the unique values for that field.
            Returns a list.
            '''
        uniques = []
        for item in self.data.__iter__():
            if item[field].strip() not in uniques:
                uniques.append(item[field].strip())
        return uniques

@app.route('/')
def index():
    app.page['url'] = 'http://interactive.nydailynews.com/project/archive/amazing-history-nyc/'
    app.page['title'] = 'The amazing history of New York City'.decode('utf-8')
    app.page['description'] = 'Explore the sinners, saints, victors, victims, lovers, lost souls, magnates, madmen, geniuses and fools who powered the epic rise of NYC.'.decode('utf-8')
    app.page['keywords'] = 'history of new york city, new york history, old new york, history of nyc, nyc history, history of new york, new york city history, manhattan history, jay maeder, big town'.decode('utf-8')
    app.page['title_fb'] = 'The amazing history of New York City'.decode('utf-8')
    app.page['description_fb'] = 'Explore the sinners, saints, victors, victims, lovers, lost souls, magnates, madmen, geniuses and fools who powered the epic rise of America’s largest metropolis.'.decode('utf-8')
    app.page['twitter'] = 'Explore the sinners, saints, geniuses and fools who powered the epic rise of NYC in this AMAZING history. http://nydn.us/historyofNYC'.decode('utf-8')
    
    with open('static/data/bigtown.json', 'rb') as jsond:
        data = json.load(jsond)

    jq = JsonQuery(data)
    yearband = jq.get_uniques('Bucket')
    response = {
        'app': app,
        'data': data,
        'yearband': yearband
    }
    return render_template('index.html', response=response)

@app.template_filter(name='last_update')
def last_update(blank):
    """ Returns the current date. That means every time the project is deployed,
        the datestamp will update.
        Returns a formatted date object, ala "Friday Feb. 20"
        """
    today = date.today()
    return today.strftime('%A %B %d')

@app.template_filter(name='timestamp')
def timestamp(blank):
    """ What's the current date and time?
        """
    today = datetime.today()
    return today.strftime("%A %B %d, %-I:%M %p")

@app.template_filter(name='ordinal')
def ordinal_filter(value):
    """ Take a number such as 62 and return 62nd. 63, 63rd etc.
        """
    digit = value % 10
    if 10 < value < 20:
        o = 'th'
    elif digit is 1:
        o = 'st'
    elif digit is 2:
        o = 'nd'
    elif digit is 3:
        o = 'rd'
    else:
        o = 'th'
    return '%d%s' % (value, o)
app.add_template_filter(ordinal_filter)

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

@app.template_filter(name='slugify')
def slugify_filter(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))
app.add_template_filter(slugify_filter)

if __name__ == '__main__':
    app.run()
