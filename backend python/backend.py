import time

from common import grabQuery
from flask import Flask
from flask_cors import CORS, cross_origin
from thormonitor_collect_data import gradDataAndSaveToDB
from thormonitor_update_ips import updateIPs
from thornode_collect_data_global import collectDataGlobal
from thormonitor_collect_data_rpc_bifrost import biFrostGrabDataAndSaveToDB

from threading import Thread

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def flaskThread():
    app.run(host='0.0.0.0', port=6000)


@app.route('/thor/api/grabData', methods=['GET'])
@cross_origin()
def grabData():
    """
    grabData is used to output the DB in json format, fires on api accesses

    return: json containing the current data from thornode_monitor and thornode_monitor_global tables
    """
    currentDBData = (grabQuery('SELECT * FROM noderunner.thornode_monitor'))
    globalData = (grabQuery('SELECT * FROM noderunner.thornode_monitor_global'))

    return {'data': currentDBData, 'globalData': globalData[0]}


def main():
    """
    main contains the main loop which simply spins every minuite and update the various DBs
    """
    worker = Thread(target=flaskThread)
    worker.start()

    while (1):
        try:
            gradDataAndSaveToDB()
            updateIPs()
            collectDataGlobal()
            biFrostGrabDataAndSaveToDB()
        except Exception as e:
            print(e)
        time.sleep(60)


if __name__ == "__main__":
    main()
