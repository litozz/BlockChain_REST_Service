from flask import Flask
from flask import request
from flask import jsonify
from block_class.BlockChainController import BlockChainController as bcc
import logging
import json
import hashlib
from flask import render_template


bcbd = bcc("http://yourbigchaindburl:9984/")


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return "Index page"
    #return render_template('index.html')


#@app.route('/calculate_hash/<_source>',methods=['GET','POST'])
def calculate_hash(_source):
    a = str(hashlib.sha256(('bi4chain' + _source).encode('utf-8')).hexdigest())
    return str(hashlib.sha256((a + 'cja').encode('utf-8')).hexdigest())

#@app.route('/get_source_credentials/<_source>', methods=['POST'])
def get_source_credentials(_source):
    id_source=calculate_hash(_source)
    tx_list=bcbd.get_all_asset_transactions(id_source)
    credential_tx=None
    for i,tx in enumerate(tx_list):
        if 'tx_type' in tx['asset']['data'].keys():
            if tx['asset']['data']['tx_type']=='credentials_generation':
                return json.dumps(tx['asset']['data'])
    return None





@app.route('/get_all_credentials',methods=['GET','POST'])
def get_all_credentials():
    return json.dumps([ {'source':tx['asset']['data']['source'], 'public_key':tx['asset']['data']['public_key']} for tx in bcbd.get_all_asset_transactions('credentials_generation')])









@app.route('/generate_keypair/<_source>', methods=['GET','POST'])
def generate_keypair(_source):
    id_source = calculate_hash(_source)
    tx_list=bcbd.get_all_asset_transactions(id_source)
    if len(tx_list) > 0 :
        return json.dumps({'error':'The key value for what are you creating keypair already exists.'})
    pair = bcbd.generate_keypair()
    result = {'public_key': pair.public_key, 'private_key': pair.private_key, 'id_source': id_source, 'source': _source, 'tx_type':'credentials_generation'}
    tx = bcbd.create_data(result, {'empty': 'empty'}, result['public_key'], result['private_key'])
    return json.dumps({'public_key': result['public_key'], 'private_key': result['private_key']})









@app.route('/retrieve_transactions', methods=['POST'])
def retrieve_transactions():
    if (request.method == "POST"):
        decoded = json.loads(request.data.decode('utf-8'))
        public_key=None
        private_key=None
        source=None
        id_source=None
        try:
            public_key=decoded['public_key']
            private_key=decoded['private_key']
            source=decoded['source']
            id_source=calculate_hash(source)
        except:
            return jsonify({'error':'You must provide public and private keys and source.'})
        criteria=None
        try:
            criteria=decoded['criteria']
        except:
            criteria=None

        credentials=json.loads(get_source_credentials(source))

        if(credentials is not None and credentials['public_key']==public_key and credentials['id_source']==id_source and credentials['private_key']==private_key):
            if(criteria is None):
                tx_list=bcbd.get_all_asset_transactions(credentials['id_source'])
                #return json.dumps([{'transaction_id':tx['id'],'asset':tx['asset']['data']} for tx in tx_list if ('tx_type' not in tx['asset']['data'].keys() ) ])
                return json.dumps([tx for tx in tx_list if ('tx_type' not in tx['asset']['data'].keys() ) ])
            else:
                tx_list=bcbd.get_all_asset_transactions(criteria)
                #return json.dumps([{'transaction_id':tx['id'],'asset':tx['asset']['data']} for tx in tx_list if(tx['asset']['data']['id_source']==id_source and 'tx_type' not in tx['asset']['data'].keys())])
                return json.dumps([tx for tx in tx_list if(tx['asset']['data']['id_source']==id_source and 'tx_type' not in tx['asset']['data'].keys())][-1])
        else:
            return jsonify({'error':'Your credentials are not valid.'})






@app.route('/retrieve_transactions_by_source/<_source>', methods=['POST'])
def retrieve_transactions_by_source(_source):
    id_source = calculate_hash(_source)
    return retrieve_transactions(id_source)




#@app.route('/retrieve_transactions', methods=['POST'])
#def retrieve_all_transactions():
#    tx_list = bcbd.get_all_transactions()
#    result=[]
#    for tx in tx_list:
#        result.append(tx)
#        logging.warning("TIPO DE TODAS LAS TRANSACCIONES: {}".format(type(tx)))
#    return jsonify(result)


@app.route('/create', methods=['POST'])
def create():
    if (request.method == "POST"):
        decoded = json.loads(request.data.decode('utf-8'))
        decoded_data = {}
        try:
            decoded_data = decoded['data']
        except KeyError:
            return json.dumps({'error': '<data> parameter is missing.'})
        decoded_metadata = {}
        try:
            decoded_metadata = decoded['metadata']
        except KeyError:
            decoded_metadata = {'empty': 'empty'}

        try:
            decoded_pub_k = decoded['public_key']
        except KeyError:
            return json.dumps({'error': '<public_key> parameter is missing.'})
        
        try:        
            decoded_pri_k = decoded['private_key']
        except KeyError:
            return json.dumps({'error': '<private_key> parameter is missing.'})

        try:
            decoded_source = decoded['source']
        except KeyError:
            return json.dumps({'error': '<source> parameter is missing.'})
        decoded_asset_id = {}

        try:
            decoded_asset_id = decoded['asset_id']
        except KeyError:
            decoded_asset_id = None

        decoded_recipients = {}
        try:
            decoded_recipients = decoded['recipients']
        except KeyError:
            decoded_recipients = None

    id_source=calculate_hash(decoded_source)
    #Credentials validation
    tx_list=bcbd.get_all_asset_transactions(id_source)
    if len(tx_list)>0:
        credential_tx=None
        for tx in tx_list:
            if 'tx_type' in tx['asset']['data'].keys():
                if tx['asset']['data']['tx_type']=='credentials_generation':
                    credential_tx=tx
                    break
        if(credential_tx==None):
            return json.dumps({'error':'Your credentials does not exist.'})

        if credential_tx['asset']['data']['id_source']==calculate_hash(decoded_source) and credential_tx['asset']['data']['public_key']==decoded_pub_k and credential_tx['asset']['data']['private_key']==decoded_pri_k:
            decoded_data['id_source']=id_source #Adding id_source to can retrieve
            logging.info('Transaction create request received:\n{}'.format(decoded_data))
            tx = bcbd.create_data(decoded_data, decoded_metadata, decoded_pub_k, decoded_pri_k, decoded_asset_id,decoded_recipients)
            logging.info('Transaction succesfully chained.')
        else:
            return json.dumps({'error':'Your credentials are not valid.'})
    else:
        return json.dumps({'error':'Your credentials does not exist.'})

    return json.dumps(tx)





# @app.route('/check_transaction',methods=['POST'])
# def check():
#     decoded = json.loads(request.data.decode('utf-8'))
#     logging.warning("DBPATH: {}".format(decoded['dbpath']))
#     logging.warning("SOURCE: {}".format(decoded['source']))
#     logging.warning("HASH: {}".format(calculate_hash(decoded['source'])))
#     id_source=calculate_hash(decoded['source'])
#     tx_list=bcbd.get_all_asset_transactions(id_source)
#     credentials_index=0
#     for i,tx in enumerate(tx_list):
#         dict_keys=tx['asset']['data'].keys()
#         if not ('tx_type' in dict_keys): #Create credentials transaction: tx_type==credentials_generation does not exists
#             #We need remove 'id_source' from transaction because this field it is not in application database, in order to compare asset as inserted.
#             del tx['asset']['data']['id_source']
#         else:
#             if(tx['asset']['data']['tx_type']=='credentials_generation'):
#                 credentials_index=i
#     #We need remove 'create credentials' transaction, because it is not in application database, it is only in bigchain.
#     del tx_list[credentials_index]
#     #End retrieving from bigchaindb


    

#     tx_for_your_application=tx_list #PROVISIONAL
#     if len(tx_list) == len(tx_db):
#         result=[]
#         for tx,tx_db in zip(tx_list,tx_list):
#             if tx == tx:
#                 logging.warning("{} VALID".format(tx['id']))
#                 result.append((tx,True))
#             else:
#                 logging.warning("{} INVALID".format(tx['id']))
#                 result.append((tx,False))
#         for (tx,r) in result:
#             logging.warning(tx['asset']['data'])
#         return jsonify(result)
#     else:
#         return json.dumps({({'error','Transaction lists have non equal lengths.'},False)})


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=11234, debug=True)
