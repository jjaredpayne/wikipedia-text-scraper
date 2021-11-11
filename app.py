from typing import KeysView
from flask import Flask, json, request, jsonify
from flask_cors import CORS, cross_origin
import wikipedia

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def home_view():
    body = "<h1>wiki-text-scraper-361</h1>"
    body += "<p>Request text from a specified Wikipedia article heading or subheading.<br>"
    body += "The microservice will search for the passed wikipage and will return the first result, if available.<br>"
    body += "The response will include all article text between the specified (sub)heading and the next (sub)heading.<br>"
    body += "If a heading is not found or specified, the article summary is returned.<br><br>"
    body += "Request:<br>https://wiki-text-scraper-361.herokuapp.com/requestText?wikipage=RequestPage&heading=RequestedHeading&sentence=SummarySentences<br><br>"
    body += 'Response:<br>[{<br>'
    body += '<div>&nbsp;&nbsp;&nbsp;&nbsp;"wikiText":"Requested Text",</div><br>'
    body += '<div>&nbsp;&nbsp;&nbsp;&nbsp;"heading":"Returned Heading"</div><br>'
    body += '<div>&nbsp;&nbsp;&nbsp;&nbsp;"page":"WikipediaPage Page Title",</div><br>'
    body += '<div>&nbsp;&nbsp;&nbsp;&nbsp;"url":"WikipediaPage URL",</div><br>'
    body += '}]</p>'
    return body

@app.route("/requestText", methods=['GET'])
def retrieveInfo():
    print("RequestText received")
    if request.method == "GET":
        # Set variables for accessing page section
        wikipage = request.args.get('wikipage', '')
        heading = request.args.get('heading', '')
        sentences = request.args.get('sentences', '')
        headingMarkUp = "== " + heading + " =="
        returnSection = {
                "wikitext": "",
                "page": "",
                "heading": ""
        }

        # Perform search for the wikipage (places results in
        # an array)
        result = wikipedia.search(wikipage, results=2)

        # if the first result doesn't work, use the 2nd result
        # if neither work, return an error
        try:
            try:
                page = wikipedia.page(result[0])
            except:
                page = wikipedia.page(result[1])
        except:
            return "Error. Wikipedia page not found."

        if heading == None :
            return wikipedia.summary(page.url, sentences=sentences)

        # When a page is found, split it into lines
        searchArray = page.content.split("\n")

        # compare each line.lower to the headingmarkup.lower and set
        # and set headingMarkUp = line for the correct capitalization
        count = 0
        for i in searchArray:
            if i.lower().find(headingMarkUp.lower()) == True:
                headingMarkUp = i
                break
            count += 1

        # split page into two elements. Element 1 holds the entirety
        # of the page after the headingMarkUp
        pageArray = page.content.split(headingMarkUp)
        returnSection['page'] = str(page)
        returnSection['url'] = str(page.url)
        returnSection['heading'] = headingMarkUp.replace("==", '').strip()

        # Add each line after the heading until the next heading is found
        # If heading not found, return page summary
        try:
            sectionArray = pageArray[1].split("\n")
        except:
            returnSection['heading'] = "Summary"
            returnSection["wikitext"] = wikipedia.summary(page.title)
            return returnSection
        
        # If heading is found, add each line to the requested text until the
        # next heading is found.
        for i in range(0, len(sectionArray)):
            if sectionArray[i].find('==') != -1:
                return returnSection
            returnSection['wikitext'] += sectionArray[i]

@app.route("/requestText", methods=['POST'])
def retrieveInfoPost():
    print("RequestText received")
    if request.method == "POST":
        body = "<h> 404. That resource is not available.</H><p>Do not POST, GET.</p>"
        return body