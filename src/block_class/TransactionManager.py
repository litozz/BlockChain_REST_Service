class TransactionManager:

	def __init__(self,_bc_driver):
		self.bc_driver = _bc_driver


	#tx_object es nuestro objeto transaccion
	def prepare_transaction(self,_tx_object,_asset_id=None,_recipients=None):
		if(_tx_object.op_type=='CREATE'):
			if(_asset_id!=None): #Puede haber transacciones CREATE referidas a un asset que ya existe
				tx_list=self.bc_driver.connection.transactions.get(asset_id=_asset_id,operation='CREATE')
				if(len(tx_list)>0): #Ya habia un elemento con ese id de asset

					#print("[PREPARE_TRANSACTION]: Entrando en CREATE, existe el asset.")
					
					asset=_tx_object.asset.data
					metadata=_tx_object.asset.md

					output_index = 0
					output = tx_list[-1]['outputs'][output_index]

					inputs = {
						'fulfillment': output['condition']['details'], #Contiene el actual propietario
						'fulfills': {
							'output_index': output_index,
							'transaction_id': tx_list[-1]['id'] #El id de la anterior transaccion
						},
						'owners_before': output['public_keys']
					}


					prepared= self.bc_driver.connection.transactions.prepare(
						operation='CREATE',
						signers=_tx_object.signer_public_key,
						asset=asset,
						metadata=metadata,
						inputs=inputs,
					)


					#print("PREPARED CREATE EXISTIENDO ASSET:\n{}".format(prepared))

					return prepared

				else:

					#print("[PREPARE_TRANSACTION]: Entrando en CREATE, existe el asset (realmente no existe el asset).")


					prepared= self.bc_driver.connection.transactions.prepare(
					    operation='CREATE',
					    signers=_tx_object.signer_public_key,
					    asset=_tx_object.asset.data,
					    metadata=_tx_object.asset.md,
					)

					#print("PREPARED CREATE NO EXISTE ASSET (en realidad no existe):\n{}".format(prepared))

					return prepared

			else: #El asset es completamente nuevo

				#print("[PREPARE_TRANSACTION]: Entrando en CREATE, NO existe el asset.")

				
				prepared= self.bc_driver.connection.transactions.prepare(
				    operation='CREATE',
				    signers=_tx_object.signer_public_key,
				    asset=_tx_object.asset.data,
				    metadata=_tx_object.asset.md,
				)

				#print("PREPARED CREATE NO EXISTE ASSET:\n{}".format(prepared))

				return prepared


		elif(_tx_object.op_type=='TRANSFER'):
			_asset_id=_tx_object.asset['id']
			_recipients=_tx_object.recipients

			if(_asset_id!=None and _recipients!=None):
				tx_list=self.bc_driver.connection.transactions.get(asset_id=_asset_id,operation='CREATE')
				if(len(tx_list)>0):

					#print("[PREPARE_TRANSACTION]: Entrando en TRANSFER, existe el asset.")

					#transfer_asset = {
				    #	'id': tx_list[-1]['id']
					#}

					output_index = 0
					output = tx_list[-1]['outputs'][output_index]

					_tx_object.inputs = {
					    'fulfillment': output['condition']['details'],
					    'fulfills': {
					        'output_index': output_index,
					        'transaction_id': tx_list[-1]['id']
					    },
					    'owners_before': output['public_keys']
					}


					#print("TRANSFER PREPARADO: ")

					prepared= self.bc_driver.connection.transactions.prepare(
					    operation='TRANSFER',
					    asset=_tx_object.asset,
					    inputs=_tx_object.inputs,
					    recipients=_tx_object.recipients
					)

					#pprint(prepared)

					return prepared
				else:
					raise AssertionError('It doesn\'t exist the asset to transfer.')

			elif (_asset_id==None or _recipients==None):
				raise AssertionError('You must specify asset id and recipients in a TRANSFER transaction.')

		else:
			raise AssertionError('Operation type must be CREATE or TRANSFER only.')




		#return self.bc_driver.connection.transactions.prepare(
		#    operation=_tx_object.op_type,
		#    signers=_tx_object.signer_public_key,
		#    asset=_tx_object.asset.data,
		#    metadata=_tx_object.asset.md
		#)


	#prep_tx es uno de los objetos transaccion que devuelve bigchaindb
	def fulfill_transaction(self,_prep_tx,_signer_private_key):
		return self.bc_driver.connection.transactions.fulfill(
		    _prep_tx,
		    private_keys=_signer_private_key
		)


	#tx es uno de los objetos transaccion que devuelve bigchaindb
	def is_transaction_fulfilled(self,_tx):
		try:
			k=_tx['inputs'][0]['fulfillment']['public_key']
			return False
		except:
			return True


	#tx es uno de los objetos transaccion que devuelve bigchaindb
	def send_transaction(self,_tx):
		if(self.is_transaction_fulfilled(_tx)):
			sent_tx = self.bc_driver.connection.transactions.send(_tx)
			assert sent_tx == _tx
			return sent_tx
		else:
			raise AssertionError('You must fulfill this transaction before send it.')


	def direct_process_tx(self,_tx_object,_signer_private_key,_asset_id=None,_recipients=None):
		if(_tx_object.op_type=='TRANSFER'):
			_asset_id=_tx_object.asset['id']
			_recipients=_tx_object.recipients
			if(_asset_id==None or _recipients==None):
				raise AssertionError('You must specify asset id and recipients in a TRANSFER transaction.')
		ptx=self.prepare_transaction(_tx_object,_asset_id,_recipients)
		ftx=self.fulfill_transaction(ptx,_signer_private_key)
		return self.send_transaction(ftx)




	#tx es uno de los objetos transaccion que devuelve bigchaindb
	def get_transaction_id(self,_tx):
		return _tx['id']


	#def get_transaction_status(self,txid):
	#	return self.bdb.transactions.status(txid).get('status')


	#tx es uno de los objetos transaccion que devuelve bigchaindb
	def get_transaction_status(self,_tx):
		return self.bc_driver.connection.transactions.status(self.get_transaction_id(_tx)).get('status')		


	def get_last_transaction(self,_asset_id):
		if(isinstance(_asset_id,list)):
			raise AssertionError('Asset id must be unique, not list.')
		return self.bc_driver.connection.transactions.get(asset_id=_asset_id)[-1]

	def get_transaction_list(self,_asset_id):
		if(isinstance(_asset_id,list)):
			raise AssertionError('Asset id must be unique, not list.')
		return self.bc_driver.connection.transactions.get(asset_id=_asset_id)

	def get_all_transactions(self):
		return self.bc_driver.connection.transactions

