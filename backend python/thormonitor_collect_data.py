import time

import requests
import json
import random
from common import commitQuery, grabQuery


def grabLatestBlockHeight(nodes):
    """
    grabLatestBlockHeight looks at 3 random nodes in the active pool and returns the max height from those 3 nodes

    :param nodes: all thor nodes currently on the network pulled from ninerelms api

    :return: the latest block height
    """
    activeNodes = [x for x in nodes if "Active" == x['status']]

    status_code = 0
    while status_code != 200:
        randomOffsets = [random.randint(0, len(activeNodes) - 1), random.randint(0, len(activeNodes) - 1),
                         random.randint(0, len(activeNodes) - 1)]

        status = []
        for i in range(0, len(randomOffsets)):
            try:
                state = requests.get('http://' + activeNodes[randomOffsets[i]]['ip_address'] + ":27147/status?",
                                     timeout=5)
                if state.status_code == 200:
                    status.append(json.loads(state.text))
            except Exception as e:
                print("timed out")

        #check if we have any blocks, if yes break from loop if not try another 3 random nodes
        if len(status) != 0:
            status_code = 200

    blocks = [x['result']['sync_info']['latest_block_height'] for x in status]

    return max(blocks)


def splitNodes(nodes):
    """
    splitNodes compares the list of nodes currently in the DB and what is returned by ninerelms API

    :param nodes: all thor nodes currently on the network pulled from ninerelms api

    :return dataForExistingNodes: list of nodes already in our DB
    :return dataForNewNodes: list of nodes not already in our DB
    """
    currentDBData = (grabQuery('SELECT * FROM noderunner.thornode_monitor'))
    fullAddrList = [x['node_address'] for x in nodes]
    currentAddrList = [x['node_address'] for x in currentDBData]
    newList = list(set(fullAddrList).symmetric_difference(set(currentAddrList)))

    dataForExistingNodes = [x for x in nodes if x['node_address'] in currentAddrList]
    dataForNewNodes = [x for x in nodes if x['node_address'] in newList]

    return dataForExistingNodes, dataForNewNodes


def gradDataAndSaveToDB():
    """
    gradDataAndSaveToDB used to update thornode_monitor_global database
    """
    response_API = requests.get('https://thornode.ninerealms.com/thorchain/nodes')
    data = json.loads(response_API.text)
    # sanitise data remove any empty elements
    nodes = [x for x in data if '' != x['node_address']]

    maxHeight = grabLatestBlockHeight(nodes)

    query = 'UPDATE noderunner.thornode_monitor_global SET maxHeight = {field} WHERE primary_key = 1;'.format(
        field=maxHeight)
    commitQuery(query)

    # check if we are in a churn

    dataForExistingNodes, dataForNewNodes = splitNodes(nodes)
    for node in dataForExistingNodes:
        query = "UPDATE noderunner.thornode_monitor SET " \
                "active_block_height = '{active_block_height}'," \
                "bond_providers = '{bond_providers}'," \
                "bond = '{bond}'," \
                "current_award = '{current_award}'," \
                "slash_points = '{slash_points}'," \
                "forced_to_leave = '{forced_to_leave}'," \
                "requested_to_leave = '{requested_to_leave}'," \
                "jail = '{jail}' ," \
                "bond_address = '{bond_address}'," \
                "observe_chains = '{observe_chains}'," \
                "preflight_status = '{preflight_status}'," \
                "status = '{status}'," \
                "status_since = '{status_since}'," \
                "version = '{version}' WHERE (node_address = '{node_address}');".format(
            active_block_height=node['active_block_height'],
            bond_providers=json.dumps(node['bond_providers']),
            bond=int(node['total_bond']),
            current_award=int(node['current_award']),
            slash_points=node['slash_points'],
            forced_to_leave=int(node['forced_to_leave']),
            requested_to_leave=int(node['requested_to_leave']),
            jail=json.dumps(node['jail']), bond_address='',
            observe_chains=json.dumps(node['observe_chains']),
            preflight_status=json.dumps(node['preflight_status']),
            status=node['status'],
            status_since=node['status_since'], version=node['version'], node_address=node['node_address'])
        commitQuery(query)

    # Loop over new nodes and grab IP addr
    for node in dataForNewNodes:
        if node['ip_address'] != "":
            response_code = 0
            while response_code != 200:
                response = requests.get("http://ip-api.com/json/" + node['ip_address'])
                response_code = response.status_code
                if response_code == 429:
                    print("rate limited wait 60seconds")
                    time.sleep(60)
                elif response_code == 200:
                    ip_data = json.loads(response.text)
                    node['ip_data'] = ip_data

        else:
            node['ip_data'] = {}
            node['ip_data']['city'] = ""
            node['ip_data']['isp'] = ""

        query = "INSERT INTO noderunner.thornode_monitor (node_address, ip_address, location, isp, " \
                "active_block_height, bond_providers, bond, current_award, slash_points,forced_to_leave, " \
                "requested_to_leave, jail, bond_address, observe_chains, preflight_status, status, " \
                "status_since, version) VALUES ('{node_address}', '{ip_address}','{city}','{isp}'," \
                "'{active_block_height}','{bond_providers}','{bond}','{current_award}','{slash_points}'," \
                "'{forced_to_leave}','{requested_to_leave}', '{jail}','{bond_address}'," \
                "'{observe_chains}','{preflight_status}','{status}','{status_since}'," \
                "'{version}')".format(node_address=node['node_address'], ip_address=node['ip_address'],
                                      city=node['ip_data']['city'], isp=node['ip_data']['isp'],
                                      active_block_height=node['active_block_height'],
                                      bond_providers=json.dumps(node['bond_providers']), bond=int(node['total_bond']),
                                      current_award=int(node['current_award']), slash_points=node['slash_points'],
                                      forced_to_leave=int(node['forced_to_leave']),
                                      requested_to_leave=int(node['requested_to_leave']),
                                      jail=json.dumps(node['jail']), bond_address='',
                                      observe_chains=json.dumps(node['observe_chains']),
                                      preflight_status=json.dumps(node['preflight_status']), status=node['status'],
                                      status_since=node['status_since'], version=node['version'])
        commitQuery(query)
