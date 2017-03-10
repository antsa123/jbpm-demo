from flask import Flask, render_template
import requests
from time import strftime

app = Flask(__name__)


@app.route('/')
def index():
    print(app.url_map)
    return render_template('index.html')


@app.route('/skyscanner/')
def haeLento():

    aika = strftime("%Y-%m-%d")
    params = {
        "apiKey" : "tu705911788977665986179742030436"
    }
    headers = {
        "Accept" : "application/json"
    }
    url = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/FI/EUR/en-GB/FI/anywhere/"+aika


    response = requests.get(url,params=params,headers=headers)



    print (response.json())
    return 'hello'

if __name__ == '__main__':

    app.run(host='127.0.0.1', port= 5004,debug=True)

