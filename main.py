from flask import Flask, render_template, request
import time, requests, re

app = Flask(__name__)

graphql_addr = "https://api.digitransit.fi/routing/v2/hsl/gtfs/v1" + \
        "?digitransit-subscription-key=754a004ba87c4fdd8506532327e212c0"

search_addr = "https://api.digitransit.fi/geocoding/v1/search"

search_params = {
        "digitransit-subscription-key": "954b08e64f1f465ba4c03d0d88cf69e2",
        "lang": "fi",
        "sources": "gtfsHSL,gtfsHSLlautta",
        "layers": "stop,station",
}

def hsl_stop_id(stop_id):
    osuma = re.search(r"HSL:[0-9]+", stop_id)
    return osuma and osuma.group(0)

def hae_pysakit(nimi_tai_osa):
    pysakit = requests.get(search_addr,
            params={**search_params, "text": nimi_tai_osa}).json()
    return {hsl_stop_id(feature['properties']['id']): feature['properties']
            for feature in pysakit['features']}

def hae_pysakkitiedot(pysakki):
    return requests.post(graphql_addr, json=dict(
        query=open("stop-query.gql").read(),
        variables=dict(
            numberOfDepartures=10,
            startTime=int(time.time()),
            stopId=pysakki,
            timeRange=3600,
        ))).json()

@app.route("/")
def root():
    return render_template('haku.html')

def aikataulusivu(pysakkitiedot):
    return render_template('aikataulu.html',
            url=pysakkitiedot['url'],
            pysahdykset=pysakkitiedot['stoptimes'],
            pysakki=pysakkitiedot['name'])

def pysakkihakusivu(haku, pysakit):
    return render_template('pysakkilista.html',
            nimi_tai_osa=haku,
            pysakit=pysakit)

@app.route("/hae")
def vastaus():
    pysakki = request.args.get('pysakki', 'HSL:1282103')
    pysakkitiedot = hae_pysakkitiedot(pysakki)['data']['stop']
    if pysakkitiedot: return aikataulusivu(pysakkitiedot)
    else: return pysakkihakusivu(pysakki, hae_pysakit(pysakki))

#if __name__ == '__main__':
#        app.run(debug=True)