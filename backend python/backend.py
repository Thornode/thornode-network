import time

from common import grabQuery
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from thormonitor_collect_data import gradDataAndSaveToDB
from thormonitor_update_ips import updateIPs
from thornode_collect_data_global import collectDataGlobal
from thormonitor_collect_data_rpc_bifrost import biFrostGrabDataAndSaveToDB
from thornode_historical_data import checkIfNewChurn
from flasgger import Swagger
from flaskTemplate import template as flaskTemplate
from flaskTemplate import swagger_config as swaggerConfig

from threading import Thread

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
swagger = Swagger(app, template=flaskTemplate,config=swaggerConfig)


def flaskThread():
    app.run(host='0.0.0.0', port=6000)


@app.route('/thor/api/grabData', methods=['GET'])
@cross_origin()
def grabData():
    """
    grabData is used to output the DB in json format, fires on api accesses
    ---
    tags:
         - General
    responses:
      200:
        description: json containing the current data from thornode_monitor and thornode_monitor_global tables
    """
    currentDBData = (grabQuery('SELECT * FROM noderunner.thornode_monitor'))
    globalData = (grabQuery('SELECT * FROM noderunner.thornode_monitor_global'))

    return {'data': currentDBData, 'globalData': globalData[0]}

@app.route('/thor/api/grabBond=<node>', methods=['GET'])
@cross_origin()
def grabBond(node):
    """Grab a nodes bond over past churns
       API used to inspect the bond amount of a node over time.
       ---
       tags:
         - Historical
       parameters:
         - name: node
           in: path
           type: string
           required: true
           default: thor1sngd0zz6pwdx2e20sml27354vzkrwa4fnjxvnc
           description: The node to look at
       responses:
         200:
           description: The bond amount of a node over past churns
       """
    data = grabQuery("SELECT * FROM noderunner.thornode_monitor_historic where node_address='{field}' ORDER BY churnHeight ASC".format(
        field=node))

    interim = {}
    for key in data:
        interim[key['churnHeight']] = key['bond']

    return jsonify(interim)

@app.route('/thor/api/grabSlashes=<node>', methods=['GET'])
@cross_origin()
def grabSlashes(node):
    """Grab a nodes slashes over past churns
       API used to inspect the slash amount of a node over time.
       ---
       tags:
         - Historical
       parameters:
         - name: node
           in: path
           type: string
           required: true
           default: thor1sngd0zz6pwdx2e20sml27354vzkrwa4fnjxvnc
           description: The node to look at
       responses:
         200:
           description: The slash amount of a node over past churns
       """
    data = grabQuery("SELECT * FROM noderunner.thornode_monitor_historic where node_address='{field}' ORDER BY churnHeight ASC".format(
        field=node))

    interim = {}
    for key in data:
        interim[key['churnHeight']] = key['slash_points']

    return jsonify(interim)

@app.route('/thor/api/grabRewards=<node>', methods=['GET'])
@cross_origin()
def grabRewards(node):
    """Grab a nodes Rewards over past churns
       API used to inspect the rewards amount of a node over time.
       ---
       tags:
         - Historical
       parameters:
         - name: node
           in: path
           type: string
           required: true
           default: thor1sngd0zz6pwdx2e20sml27354vzkrwa4fnjxvnc
           description: The node to look at
       responses:
         200:
           description: The rewards amount of a node over past churns
       """
    data = grabQuery("SELECT * FROM noderunner.thornode_monitor_historic where node_address='{field}' ORDER BY churnHeight ASC".format(
        field=node))

    interim = {}
    for key in data:
        interim[key['churnHeight']] = key['current_award']

    return jsonify(interim)

@app.route('/thor/api/versions', methods=['GET'])
@cross_origin()
def grabVersion():
    """Grab the versions of active nodes on the network
       ---
       tags:
         - General
       responses:
         200:
           description: the breakdown of node versions on the network
       """
    data = grabQuery('SELECT * FROM noderunner.thornode_monitor where status="Active"')

    output = {}
    for key in data:
        if key["version"] not in output:
            output[key["version"]] = 1
        else:
            output[key["version"]] += 1

    return jsonify(output)

@app.route('/thor/api/locations', methods=['GET'])
@cross_origin()
def grabLocation():
    """Grab the hosted country of Active and Standby nodes on the network
       ---
       tags:
         - General
       responses:
         200:
           description: the breakdown of node locations on the network
       """
    data = grabQuery('SELECT * FROM noderunner.thornode_monitor where status="Active" OR status="Standby"')

    output = {}
    for key in data:
        if key["country"] != '':
            if key["country"] not in output:
                output[key["country"]] = 1
            else:
                output[key["country"]] += 1

    return jsonify(output)

@app.route('/thor/api/grabPosition=<node>', methods=['GET'])
@cross_origin()
def grabPositions(node):
    """Grab a nodes relative performance over past churns
       API returns the position out of others based on slashes from previous churns. positions 1-max (number of nodes in churn) 1 being lowest/best.

       0 = Not active that churn
       ---
       tags:
         - Historical
       parameters:
         - name: node
           in: path
           type: string
           required: true
           default: thor1sngd0zz6pwdx2e20sml27354vzkrwa4fnjxvnc
           description: The node to look at
       responses:
         200:
           description: The node position compared to other active nodes over past churns
       """
    data = grabQuery(
        "SELECT * FROM noderunner.thornode_monitor_historic where node_address='{field}' ORDER BY churnHeight ASC".format(
            field=node))

    interim = {}
    for key in data:
        interim[key['churnHeight']] = {}
        interim[key['churnHeight']]['position'] = key['position']
        interim[key['churnHeight']]['max'] = key['maxNodes']

    return jsonify(interim)

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
            checkIfNewChurn()
        except Exception as e:
            print(e)
        time.sleep(60)


if __name__ == "__main__":
    main()
