from typing import KeysView
from flask import Flask, request, jsonify
import json
import urllib.parse
import pywikibot
from pywikibot import textlib
import mwparserfromhell
import wikitextparser
from flask_cors import CORS
import re
import wikipedia

app = Flask(__name__)
CORS(app)


@app.route("/requestText", methods=['GET', 'POST'])
def retrieveInfo():
    print("RequestText received")
    if request.method == "GET":
        wikipage = request.args.get('wikipage', '')
        heading = request.args.get('heading', '')

    print('wikipage: ' + wikipage)
    # Search for page and use the first result
    result = wikipedia.search(wikipage)
    page = wikipedia.suggest(wikipage)
    print('wikipage result 0: ' + result[0])

    try:
        page = wikipedia.page(result[0])
    except:
        page = wikipedia.page(result[1])

    headingMarkUp = "=== " + heading.lower() + " ==="

    sectionArray = page.content.split("\n")

    count = 0
    for i in sectionArray:
        if sectionArray[count].find(headingMarkUp):
            print(sectionArray[count])
            return sectionArray[count]
        count += 1

    # # Creates Wikipedia site object
    # site = pywikibot.Site('wikipedia:en')

    # # Creates Wikipedia page Object
    # page = pywikibot.Page(site, wikipage)
    # text = page.text
    # count = 0

    # # Look for Redirect and update destination if found
    # for i in wikitextparser.parse(text).sections:
    #     sectiontext = str(wikitextparser.parse(text).sections[count])
    #     print("Section" + str(count) + " "
    #           + str(wikitextparser.parse(text).sections[count]))
    #     count += 1
    #     if re.search("REDIRECT", sectiontext):
    #         print("Redirect found")
    #         print(re.search(r'\[\[(.*?)\]\]', sectiontext))
    #         newpage = re.search(r'\[\[(.*?)\]\]', sectiontext)
    #         newpage = newpage.group()
    #         newpage = newpage.replace("[[", "")
    #         newpage = newpage.replace("]]", "")
    #         print(newpage)
    #         page = pywikibot.Page(site, newpage)
    #         text = page.text
    #         break
    #         print(text)

    # # Look for heading in each section
    # count = 0
    # for i in wikitextparser.parse(text).sections:
    #     print("Section" + str(count) + " " + str(wikitextparser.parse(text).sections[count]))
    #     sectionText = str(wikitextparser.parse(text).sections[count])
    #     if ("=="+heading).lower() in sectionText.lower():
    #         print("heading " + heading + " Found!")
    #         textJSON = {"text": str(wikitextparser.parse(text).sections[0])}
    #         print(textJSON)
    #         return jsonify(textJSON)
    #     count += 1
    # return ''
