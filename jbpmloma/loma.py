from flask import Flask, render_template, request
import requests
import datetime
import json
from random import randrange, randint, choice
import sys

app = Flask(__name__)

# Kirjanpito käynnissä oleville prosesseille
liveProcesses = []

# Tähän voi muuttaa oman osoitteemsa jbpm:n alustalle
url_jbpm= "http://localhost:8080/jbpm-console/"

headers_jbpm = {
        "Accept": "application/json",
        "Authorization": "Basic YWRtaW46YWRtaW4=" # admin - admin
}

@app.route('/')
def index():
    # Aloitussivu
    return render_template('index.html')


@app.route('/start')
def startProcess():


    url = url_jbpm+"rest/runtime/com.demounit:ASE-6050-Demo:1.0/process/ASE-6050-Demo.lentolippu/start"

    # Aloitetaan jbpm prosessi

    response = requests.post(url, headers=headers_jbpm)
    json_in = response.json()

    # Otetaan porcessID talteen
    processID = str(json_in["id"])

    # Pidetään kirjaa
    liveProcesses.append(processID)

    return json.dumps({"ProcessID": processID})


@app.route('/abort')
def abortProcess():
    
    #Prosessi ID voidaan laittaa POST parametrina client puolelta!
    processID = request.args.get("ID")

    # keskeytetään prosessi jos käynnissä
    if (processID in liveProcesses):

        liveProcesses.remove(processID)
        url = url_jbpm+"rest/runtime/com.demounit:ASE-6050-Demo:1.0/process/instance/"+processID+"/abort"
        response = requests.post(url, headers=headers_jbpm)
        # json_in = response.json()

    return 'aborted'


@app.route('/finish')
def finishProcess():

    #Lippu ostettu
    processID = request.args.get("ID")
    Result = request.args.get("Result")

    taskID = (nextTask(processID))
    startTask(taskID)
    completeTask(taskID,Result)

    return 'finished'

@app.route('/skyscanner/')
def haeLento():

    processID = request.args.get("ID")
    Result = request.args.get("Result")

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time = datetime.datetime.strftime(tomorrow,"%Y-%m-%d")

    print(len(sys.argv))
    if (len(sys.argv) == 2):
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

    # Demoa varten --> voidaan ohjata tänne antamalla ylimääräinen sys.argv
    else:
        demo_prices = ["54", "115", "270", "334", "701", "1302", "2700" ]
        demo_destinations = ["Copenhagen", "Berlin", "Madeira", "Moscow", "Osaka", "Auckland", "Tahiti"]
        demo_departures = ["07:45", "11:30", "16:20", "18:15", "01:00", "19:00", "04:35"]

        pick = randrange(0,len(demo_prices))
        offer = {'start': "Helsinki-Vantaa", 'stop': demo_destinations[pick], 'aika': demo_departures[pick], 'hinta': demo_prices[pick]}

    # Suoritetaan eka taski tässä
    taskID = nextTask(processID)
    startTask(taskID)
    completeTask(taskID,Result)

    return json.dumps(offer)

def chooseOffer(json_in):

    price = 0
    origin = 'Helsinki'
    destination = 'None'
    time = '10:00:00'

    # Onko tänään tarjouksia?
    if len(json_in['Quotes']) != 0:

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


    return offer

def startTask(taskID):

    # Aloitetaan jbpm task

    url = url_jbpm+"rest/task/"+taskID+"/start"
    response = requests.post(url, headers=headers_jbpm)
    # json_in = response.json()

    return

def nextTask(processID):

    # Haetaan prosessin seuraava taski
    url = url_jbpm+"rest/task/query?processInstanceId=" + processID
    response = requests.get(url, headers=headers_jbpm)
    json_in = response.json()

    # Parsitaan talteen seuraava processId:n taski
    nextTaskID = json_in["taskSummaryList"][len(json_in["taskSummaryList"])-1]["id"]

    return str(nextTaskID)

def completeTask(taskID,Result):


    #Suoritetaan jbpm task
    url = url_jbpm+"rest/task/" + taskID + "/complete/?map_hyvaksytty_out="+Result
    response = requests.post(url, headers=headers_jbpm)
    # json_in = response.json()

    return

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=int(sys.argv[1]), threaded=True, debug=True)

