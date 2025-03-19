from flask import Flask, render_template, request
import time, requests

app = Flask(__name__)

API_osoite = "https://api.digitransit.fi/routing/v2/hsl/gtfs/v1" + \
        "?digitransit-subscription-key=754a004ba87c4fdd8506532327e212c0"

def hae_pysakkitiedot(pysakki):
    return requests.post(API_osoite, json=dict(
        query=open("stop-query.gql").read(),
        variables=dict(
            numberOfDepartures=10,
            startTime=int(time.time()),
            stopId=pysakki,
            timeRange=3600,
        ))).json()

@app.route("/")
def root():
    return render_template('lomake.html')

@app.route("/vastaus")
def vastaus():
    return render_template('vastaus.html',
            pysakki=request.args.get('pysakki', 'Maunula'))

