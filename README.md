# Thornode Monitor

The Monitor dashboard is used to collate information on active, standby and old nodes on the rune network it collates information
from multiple sources and displays them on a single dashboard. This repo consists of both the front end (js react app) 
and the backend module (a python api server).

1) Front end:
  - This is all the code in this repository, minus the lambda functions folder and python backend folder
  - Built using react
  - It pulls data from the backend api

2) Back end:
  - Several parts to the backend
    1) mySQL database to store all the data
    2) python app responsible to collect data and provide an api access point to the front end


  - The database is fairly simple and consists of 2 tables with the following structure
    

    - thornode_monitor_global - holds network information
      - primary_key - int
      - maxHeight - int (current blockheight used to pull other data)
      - retiring - boolean (indicates if a vault is retiring)
      - coingecko - string (json string containing price/trading info pulled from coingecko api)
      - lastChurn - int (block of last churn)
      - secondsPerBlock - float
      - churnInterval - int
      - BadValidatorRedline - int
    

    - thornode_monitor - holds information on each node in the network
      - node_address - string (primary key)
      - active_block_height - int (block at which the node became active)
      - bond_provider - string (json string containing information on bonds and providers)
      - bond -int (amount bonded)
      - current_award - int (amount awarded this epoch)
      - slash_points - int (slash points this epoch)
      - forced_to_leave - boolean
      - requested_to_leave - boolean
      - jail - string (json string containing information on any past jailing)
      - observe_chains - string (json string containing block heights for downstream chains)
      - preflight_status - string
      - status - string
      - status_since - int
      - version - string
      - ip_address - string
      - location - string
      - isp - string
      - rpc - string (json string of response from health rpc calls)
      - bifrost - string (bifrost p2pid)


  - The python app runs off a main loop which pulls data every 20 seconds and updates the DB, it listens to api calls to
  /api/grabData and returns the data in json.  


# Old deployment via AWS lambda (no longer maintained in this fork)

There are several moving parts to this dashboard

1) Front end:
  - This is all the code in this repository, minus the lambda functions folder
  - Built using react
  - It calls an AWS API Gateway to collect data which it then displays

2) Back end:
  - Several parts to the backend
    1) AWS RDS database to store all the data
    2) AWS Lambda functions which collect the data and also provides the function for the api call
    3) AWS API Gateway which invokes one of the lambda functions to return the data to the front end

  - Back end lambda functions are in the 'lambda functions' folder, they consist of
    1) thormonitor_collect_data2: This function stores data about the nodes, ie bond, slash points status etc... into the DB
    2) thormonitor_collect_data_rpc_bifrost: This function checks the RPC and Bifrost API of each node and stores in the DB
    3) thornode_collect_data_global: This function stores info like block time per second and data from coingecko into the DB
    4) thormonitor: This is the lambda function which is invoked by the API call to return all the data to the front end from the DB



How to build:

1) ~ git clone https://github.com/thorchain/thornode-network.git
2) ~ cd thornode-network
3) ~ npm install
4) Upload the 4 functions to lambda and set them up to run every 1 minute except for the thormonitor code.
5) Create an AWS API Gateway that invokes thormonitor lambda function
6) Create aws-export.js in the src folder and enter the details of your AWS API Gateway
7) If your have populated your database with some data, all you need to do is '~ npm run start' and the front end should start pulling and displaying the data
