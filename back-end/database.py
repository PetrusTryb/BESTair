import sqlite3
import threading

LIMIT = 9999999
t_lock = threading.Lock()


def lock(func):
    def wrapper(*args, **kwargs):
        t_lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            t_lock.release()

    return wrapper


class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    @lock
    def fetchall(self, sql: str, parameters=()):
        return list(map(dict, self.cursor.execute(sql, parameters).fetchall()))

    @lock
    def fetchone(self, sql: str, parameters=()):
        data = self.cursor.execute(sql, parameters).fetchone()
        if data is None:
            return None
        return dict(data)

    def getAllStations(self, limit=LIMIT, offset=0):
        return self.fetchall('SELECT * FROM stations LIMIT ?,?', (offset, limit))

    def getStation(self, station_id):
        return self.fetchone('SELECT * FROM stations WHERE id = ?', (station_id,))

    def getPollutions(self, dateFrom, dateTo, offset):
        return self.fetchall('SELECT * FROM pollution WHERE date >= ? AND date <= ? LIMIT ?,?',
                             (dateFrom, dateTo, offset, LIMIT))

    def getPollutionsByStation(self, station_id, dateFrom, dateTo, offset):
        print(f"SELECT * FROM pollution WHERE station_id IN ({station_id}) AND date >= '{dateFrom}' AND date <= '{dateTo}' LIMIT {offset}, {LIMIT}")
        return self.fetchall(f'SELECT * FROM pollution WHERE station_id IN ({station_id}) AND date >= ? AND date <= ? LIMIT ?,?',
                             (dateFrom, dateTo, offset, LIMIT))
