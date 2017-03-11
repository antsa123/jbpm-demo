from flask import Flask, render_template
import requests
import datetime
import json
from random import randrange

app = Flask(__name__)

headers_jbpm = {
        "Accept": "application/json",
        "Authorization": "Basic YWRtaW46YWRtaW4="
}

@app.route('/')
def index():

    #print(app.url_map)
    return render_template('index.html')


@app.route('/start')
def startProcess():


    url = "http://localhost:8080/jbpm-console/rest/runtime/com.demounit:ASE-6050-Demo:1.0/process/ASE-6050-Demo.lentolippu/start"

    # aloitetaan jbpm prosessi

    response = requests.post(url, headers=headers_jbpm)
    json_in = response.json()

    # Otetaan porcessID talteen
    prosessiID = json_in["id"]

    # Haetaan seuraava taskID

    #Kokeilua ---------------------------------------------------------------
    seuraava = (nextTask(prosessiID))
    startTask(seuraava)
    completeTask(seuraava)
    seuraava = (nextTask(prosessiID))
    startTask(seuraava)
    completeTask(seuraava)


    return 'response'


@app.route('/abort')
def abortProcess():

    #miten prosessi ID tänne
    prosessiID = 0

    #keskeytetään prosessi
    url = "http://localhost:8080/jbpm-console/rest/runtime/com.demounit:ASE-6050-Demo:1.0/process/instance/"+str(prosessiID)+"/abort"
    response = requests.post(url, headers=headers_jbpm)
    json_in = response.json()


    #poistetaan prosessiId kirjanpidosta
    return 'aborted'

@app.route('/finish')
def finishProcess():

    #lippu ostettu

    return 'finished'

@app.route('/check')
def checkOffer():

    #tarjous katsottu

    return 'checked'

def startTask(taskID):

    #Aloita jbpm task [POST]

    url = "http://localhost:8080/jbpm-console/rest/task/"+str(taskID)+"/start"
    response = requests.post(url, headers=headers_jbpm)
    json_in = response.json()

    return

def nextTask(processID):

    url = "http://localhost:8080/jbpm-console/rest/task/query?processInstanceId=" + str(processID)
    response = requests.get(url, headers=headers_jbpm)
    json_in = response.json()

    # Parsitaan talteen seuraava processId:n taski


    #Toka taski vuorossa
    if (len(json_in["taskSummaryList"]) == 2):
        nextTaskID = json_in["taskSummaryList"][1]["id"]

    # Eka taski
    else:
        nextTaskID = json_in["taskSummaryList"][0]["id"]

    print(nextTaskID)
    return nextTaskID

def completeTask(taskID):

    #Suorita jbpm task [POST]
    url = "http://localhost:8080/jbpm-console/rest/task/" + str(taskID) + "/complete/?map_hyvaksytty_out=true"
    response = requests.post(url, headers=headers_jbpm)
    json_in = response.json()

    return


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

