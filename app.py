from typing import KeysView
from flask import Flask, request, jsonify
# from app.main import app
from flask_cors import CORS, cross_origin
import wikipedia

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
#@cross_origin
def home_view():
        return "<h1>wiki-text-scraper-361</h1>"

@app.route("/requestText", methods=['GET', 'POST'])
#@cross_origin()
def retrieveInfo():
    print("RequestText received")
    if request.method == "GET":
        # Set variables for accessing page section
        wikipage = request.args.get('wikipage', '')
        heading = request.args.get('heading', '')
        headingMarkUp = "== " + heading + " =="

        # Perform search for the wikipage (places results in
        # an array)
        result = wikipedia.search(wikipage)

        # if the first result doesn't work, use the 2nd result
        # if neither work, return an error
        try:
            try:
                page = wikipedia.page(result[0])
            except:
                page = wikipedia.page(result[1])
        except:
            return "Error. Wikipedia article not found."

        # When a page is found, split it into lines
        searchArray = page.content.split("\n")

        count = 0
        # compare each line.lower to the headingmarkup.lower and set
        # and set headingMarkUp = line for the correct capitalization
        for i in searchArray:
            if i.lower().find(headingMarkUp.lower()) == True:
                headingMarkUp = i
                break
            count += 1

        # split page into two elements. Element 1 holds the entirety
        # of the page after the headingMarkUp
        pageArray = page.content.split(headingMarkUp)

        # Add each line after the heading until the next section markup is found
        try:
            sectionArray = pageArray[1].split("\n")
        except:
            wikipedia.summary(page)
        returnSection = ''
        for i in range(0, len(sectionArray)):
            if sectionArray[i].find('==') != -1:
                return returnSection
            returnSection += sectionArray[i]

    # for i in sectionArray:
    #     print("sectArray index: " + sectionArray[count])
    #     if sectionArray[count].find(headingMarkUp) == True:
    #         print("Heading found")

    #         break
    #     count += 1
    # return "Not Found. Please revise your search criteria"

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
