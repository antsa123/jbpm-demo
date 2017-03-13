from flask import Flask, render_template, request
import requests
import datetime
import json
from random import randrange

app = Flask(__name__)

# Kirjanpito käynnissä oleville prosesseille
liveProcesses = []

headers_jbpm = {
        "Accept": "application/json",
        "Authorization": "Basic YWRtaW46YWRtaW4="
}

@app.route('/')
def index():

    #print(app.url_map)!
    return render_template('index.html')


@app.route('/start')
def startProcess():


    url = "http://localhost:8080/jbpm-console/rest/runtime/com.demounit:ASE-6050-Demo:1.0/process/ASE-6050-Demo.lentolippu/start"

    # aloitetaan jbpm prosessi

    response = requests.post(url, headers=headers_jbpm)
    json_in = response.json()

    # Otetaan porcessID talteen
    processID = json_in["id"]

    #pidetään kirjaa
    liveProcesses.append(processID)

    return json.dumps({"ProcessID": processID})


@app.route('/abort')
def abortProcess():
    
    #Prosessi ID voidaan laittaa POST parametrina client puolelta!
    processID = request.args.get("ID")

    # keskeytetään prosessi jos käynnissä
    if (processID in liveProcesses):

        liveProcesses.remove(processID)
        url = "http://localhost:8080/jbpm-console/rest/runtime/com.demounit:ASE-6050-Demo:1.0/process/instance/"+processID+"/abort"
        response = requests.post(url, headers=headers_jbpm)
        # json_in = response.json()

    return 'aborted'


@app.route('/finish')
def finishProcess():

    #lippu ostettu
    processID = request.args.get("ID")

    taskID = (nextTask(processID))
    startTask(taskID)
    completeTask(taskID)

    return 'finished'


@app.route('/skyscanner/')
def haeLento():

    processID = request.args.get("ID")

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time = datetime.datetime.strftime(tomorrow,"%Y-%m-%d")
    params = {
        "apiKey" : "tu705911788977665986179742030436"
    }
    headers = {
        "Accept" : "application/json"
    }
    url = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/FI/EUR/en-GB/FI/anywhere/"+time


    response = requests.get(url,params=params,headers=headers)
    json_in = response.json()
    offer = chooseOffer(json_in)


    """Suoritetaan eka taski tässä"""
    taskID = nextTask(processID)
    startTask(taskID)
    completeTask(taskID)

    return json.dumps(offer)

def chooseOffer(json_in):

    price = 1000
    origin = 'Helsinki'
    destination = 'Dubai'
    time = '10:00:00'

    if 'Quotes' in json_in:

        destinationList = json_in['Quotes']


        randomDestination = destinationList[randrange(0, len(destinationList))]

        price = str(randomDestination['MinPrice'])
        originID = randomDestination['OutboundLeg']['OriginId']
        destinationID = randomDestination['OutboundLeg']['DestinationId']
        time = str(randomDestination['QuoteDateTime']).split('T')
        time = time[1]

        for place in json_in['Places']:
            if (place['PlaceId'] == originID):
                origin = place['Name']
            elif (place['PlaceId'] == destinationID):
                destination = place['Name']

    offer = {'start': origin, 'stop': destination, 'aika': time, 'hinta': price}
    print(offer)

    return offer

def startTask(taskID):

    #Aloita jbpm task [POST]

    url = "http://localhost:8080/jbpm-console/rest/task/"+taskID+"/start"
    response = requests.post(url, headers=headers_jbpm)
    # json_in = response.json()

    return

def nextTask(processID):

    url = "http://localhost:8080/jbpm-console/rest/task/query?processInstanceId=" + processID
    response = requests.get(url, headers=headers_jbpm)
    json_in = response.json()

    # Parsitaan talteen seuraava processId:n taski
    nextTaskID = json_in["taskSummaryList"][len(json_in["taskSummaryList"])-1]["id"]

    print(nextTaskID)
    return str(nextTaskID)

def completeTask(taskID):

    #Suorita jbpm task [POST]
    url = "http://localhost:8080/jbpm-console/rest/task/" + taskID + "/complete/?map_hyvaksytty_out=true"
    response = requests.post(url, headers=headers_jbpm)
    # json_in = response.json()

    return



if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000,debug=True)

