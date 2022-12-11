#!./pyenv/bin/python
from flask import Flask
from flask import request
from datetime import datetime
from geopy import distance
from database import Database
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from flask_cors import CORS

app = Flask(__name__)
databaseName = 'data.db'
cors = CORS(app)


class DI(containers.DeclarativeContainer):
    database = providers.Singleton(Database, database_name=databaseName)


def stringToDatetime(dateStr):
    try:
        if len(dateStr) > 10:
            return datetime.strptime(dateStr, "%d-%m-%Y %H:%M:%S")
        return datetime.strptime(dateStr, "%d-%m-%Y")
    except ValueError as e:
        return datetime(2000, 1, 1)


def stringToFloat(str, defValue=0.0):
    try:
        return float(str)
    except ValueError as e:
        return defValue


def getInfo(args):
    dateFromStr = args.get('from') or '01-01-2000'
    dateToStr = args.get('to') or '31-12-2021'
    dateFrom = stringToDatetime(dateFromStr)
    dateTo = stringToDatetime(dateToStr)
    indicator = args.get('indicator') or ''
    return dateFrom, dateTo, indicator


def calcDistance(lat1, lon1, lat2, lon2):
    if lat1 > 90 or lat1 < -90:
        lat1 = 0
    if lat2 > 90 or lat2 < -90:
        lat2 = 0
    if lon1 > 180 or lon1 < -180:
        lon1 = 0
    if lon2 > 180 or lon2 < -180:
        lon2 = 0
    return distance.distance((lat1, lon1), (lat2, lon2)).km


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/pollution')
@inject
def pollution(database: Database = Provide[DI.database]):
    dateFrom, dateTo, *_ = getInfo(request.args)
    offset = request.args.get('offset') or 0
    data = database.getPollutions(dateFrom, dateTo, offset)
    if data is None:
        return 'Not found', 404
    return data


@app.route('/pollution/<stationId>')
@inject
def pollutionByStation(stationId, database: Database = Provide[DI.database]):
    dateFrom, dateTo, *_ = getInfo(request.args)
    offset = request.args.get('offset') or 0
    data = database.getPollutionsByStation(stationId, dateFrom, dateTo, offset)
    if data is None:
        return 'Station not found', 404
    return data


@app.route('/station')
@inject
def station(database: Database = Provide[DI.database]):
    offset = request.args.get('offset') or 0
    limit = request.args.get('limit') or 50
    return database.getAllStations(limit, offset)


@app.route('/station/<stationId>')
@inject
def stationId(stationId, database: Database = Provide[DI.database]):
    data = database.getStation(stationId)
    if data is None:
        return 'Station not found', 404
    return data


@app.route('/nearby')
@inject
def nearbyStation(database: Database = Provide[DI.database]):
    latitude = stringToFloat(request.args.get('latitude') or 54.372, 54.372)
    longitude = stringToFloat(request.args.get('longitude') or 18.638, 18.638)
    maxDistance = stringToFloat(request.args.get('maxDistance') or 100, 100)
    filters = getInfo(request.args)
    stations = database.getAllStations()
    stationsJSON = []
    pollutionsToGet = []
    for station in stations:
        dist = calcDistance(latitude, longitude, station['latitude'], station['longitude'])
        if dist <= maxDistance:
            station['distance'] = dist
            station['pollution'] = []
            pollutionsToGet.append(str(station['id']))
            stationsJSON.append(station)
    pollutions = database.getPollutionsByStation(", ".join(pollutionsToGet), filters[0], filters[1], 0)
    for station in stationsJSON:
        for pollution in pollutions:
            if pollution['station_id'] == station['id']:
                station['pollution'].append(pollution)
                pollutions.remove(pollution)
    finalJSON = list(filter(lambda x: len(x['pollution']) > 0, stationsJSON))
    return finalJSON


if __name__ == '__main__':
    di = DI()
    di.wire(modules=[__name__])
    app.config["JSON_SORT_KEYS"] = False
    app.run(host='0.0.0.0', port=5000)
