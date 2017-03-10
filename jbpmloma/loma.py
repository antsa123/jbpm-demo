from flask import Flask, render_template
import requests
import datetime
import json
from random import randrange
from time import strftime

app = Flask(__name__)


@app.route('/')
def index():
    print(app.url_map)
    return render_template('index.html')


@app.route('/start')
def startProcess():

    #aloitetaan jbpm prosessi
    #

    return 'hello'


@app.route('/abort')
def abortProcess():

    #keskeytetään prosessi

    return 'hello'

@app.route('/finish')
def finishProcess():

    #lippu ostettu

    return 'hello'


@app.route('/skyscanner/')
def haeLento():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    aika = datetime.datetime.strftime(tomorrow,"%Y-%m-%d")
    params = {
        "apiKey" : "tu705911788977665986179742030436"
    }
    headers = {
        "Accept" : "application/json"
    }
    url = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/FI/EUR/en-GB/FI/anywhere/"+aika


    response = requests.get(url,params=params,headers=headers)
    json_in = response.json()
    hinta = 1000
    lahtomaa = 'Helsinki'
    kohdemaa = 'Dubai'
    aika = '10:00:00'

    if 'Quotes' in json_in:

        kohdelista = json_in['Quotes']
        #print(len(kohdelista))
        #kohde = kohdelista[4]

        kohde = kohdelista[randrange(0,len(kohdelista))]

        hinta = str(kohde['MinPrice'])
        lahtoID = kohde['OutboundLeg']['OriginId']
        kohdeID = kohde['OutboundLeg']['DestinationId']
        aika = str(kohde['QuoteDateTime']).split('T')
        aika = aika[1]
        for place in json_in['Places']:
            if (place['PlaceId'] == lahtoID):
                 lahtomaa = place['Name']
            elif (place['PlaceId'] == kohdeID):
                kohdemaa = place['Name']

    output = json.dumps({'start':lahtomaa, 'stop':kohdemaa, 'aika':aika, 'hinta':hinta})
    print(output)

    return output

if __name__ == '__main__':

    app.run(host='127.0.0.1', port= 5012,debug=True)

