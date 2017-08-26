# BlockChain_REST_Service Documentation

To use this BlockChain REST service, follow this guide: 

1. First step is build the BlockChain_REST_Service image docker. For this we move to BlockChain_REST_Service
(cloned) directory and run the command `sudo docker build - -t "bcdb_service" < Dockerfile.dev`.

2. Next step is clone BigChainDB server official repo: https://github.com/bigchaindb/bigchaindb
and overwrite the `docker-compose.yml` with the one in my repo. Now you have ready BigChainDB server.

3. In your work directory, you must have the official BigChainDB server repo overwrited and this repo, as follows:
    ```
    Your_work_directory
    |____BlockChain_Rest_Service
    |____bigchaindb
    ```
    
4. Edit the overwritten docker-compose.yml. Uncoment the `bcdb_service` block, that manages the bcdb_service
behaviour, and configure it agree to your preferences (ips, ports, directories...). It is instinctive.

5. Edit the `BlockChain_REST_Service/src/app.py` file. In the `bcbd = bcc("http://yourbigchaindburl:9984/")` line,
change the domain reserved and port you gave in the last step in the URL. If you want to test it in localhost,
you must, obviously, change `yourbigchaindburl` for `localhost` or `127.0.0.1`.

6. Finished. If you want to run BigChainDB server and Flask application, you must go to bigchaindb directory and run in a terminal
`docker-compose up`. If you did all right, it will start properly everything.
