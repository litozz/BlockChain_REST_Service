from .BigChainDBDriver import BigChainDBDriver
from .AssetManager import AssetManager
from .TransactionManager import TransactionManager
from .Asset import Asset
from .KeyPair import KeyPair
from .TransactionTransfer import TransactionTransfer
from .TransactionCreate import TransactionCreate
import logging
from time import sleep

class BlockChainController:

	def __init__(self,_url_root):
		self.bdb_driver=BigChainDBDriver(_url_root)
		self.asset_manager=AssetManager(self.bdb_driver)
		self.transaction_manager=TransactionManager(self.bdb_driver)



	#direct method to CREATE transaction
	def create_data(self, _data, _md, _signer_pub_k,_signer_priv_k,_asset_id=None,_recipients=None):
		asset=self.asset_manager.create_asset(_data,_md)
		tc=TransactionCreate(_signer_pub_k,asset)
		return self.transaction_manager.direct_process_tx(tc,_signer_priv_k,_asset_id=_asset_id,_recipients=_recipients)


	#direct method to TRANSFER transaction
	def transfer_data(self, _primary_key, _signer_pub_k,_recipient_pub_k,_signer_priv_k,_unique=True):
		assets_id=self.asset_manager.search_asset_id(_primary_key,_unique)
		print(assets_id)
		if(_unique):
			tt=TransactionTransfer(assets_id,_recipient_pub_k)
			return [self.transaction_manager.direct_process_tx(tt,_signer_priv_k,assets_id)]
		else:
			tx_affected=[]
			for asset_id in assets_id:
				tt=TransactionTransfer(asset_id,_recipient_pub_k)
				tx_affected.append(self.transaction_manager.direct_process_tx(tt,_signer_priv_k,asset_id))
			return tx_affected


	def get_all_asset_transactions(self,_str_criteria):
		ids_asset=self.search_assets_id(_str_criteria,False)
		logging.warning("NUMERO DE ASSETS: {} STR_CRIT: {}".format(len(ids_asset),_str_criteria))
		tx_list=[]
		for id_asset in ids_asset:
			tx_l=self.get_transaction_list(id_asset)
			for tx in tx_l:
				tx_list.append(tx)	
		return tx_list
			
	#def get_all_transactions(self):
	#	return self.transaction_manager.get_all_transactions()




	#Mid-Grained methods

	def generate_keypair(self):
		return KeyPair()


	def create_asset(self,_data,_md):
		return self.asset_manager.create_asset(_data, _md)


	def transaction_create(self,_signer_pub_k,_signer_priv_k,_asset):
		tc=TransactionCreate(_signer_pub_k,_asset)
		return self.transaction_manager.direct_process_tx(tc,_signer_priv_k)

	def transaction_transfer(self,_recipient_pub_k,_signer_priv_k,_asset_id):
		tt=TransactionTransfer(_asset_id,_recipient_pub_k)
		return self.transaction_manager.direct_process_tx(tt,_signer_priv_k,_asset_id)




	#Fine-grained methods



	#AssetManager methods
	def search_assets(self,_str_criteria,_unique=False):
		return self.asset_manager.search_assets(_str_criteria,_unique)
	

	def search_assets_id(self,_str_criteria,_unique=False):
		return self.asset_manager.search_asset_id(_str_criteria,_unique)

	def get_asset_by_id(self,_asset_id):
		return self.asset_manager.get_asset_by_id(_asset_id)


	#def search_assets_metadata(self,_str_criteria,_unique=False):
	#	return self.asset_manager.search_asset_metadata(_str_criteria,_unique)


	def get_last_transaction(self,_asset_id):
		return self.asset_manager.get_last_transaction(_asset_id)
	

	def get_ownership(self,_asset_id):
		return self.asset_manager.get_ownership(_asset_id)	


	def get_previous_owners(self,_asset_id):
		return self.asset_manager.get_previous_owners(_asset_id)









	#TransactionManager methods
	def prepare_transaction(self,_tx_object,_asset_id=None,_recipients=None):
		return self.transaction_manager.prepare_transaction(_tx_object,_asset_id,_recipients)


	def fulfill_transaction(self,_prep_tx,_signer_private_key):
		return self.transaction_manager.fulfill_transaction(_prep_tx,_signer_private_key)



	def is_transaction_fulfilled(self,_tx):
		return self.transaction_manager.is_transaction_fulfilled(_tx)



	def send_transaction(self,_tx):
		return self.transaction_manager.send_transaction(_tx)


	def direct_process_tx(self,_tx_object,_signer_private_key,_asset_id=None,_recipients=None):
		return self.transaction_manager.direct_process_tx(_tx_object,_signer_private_key,_asset_id,_recipients)


	def get_transaction_id(self,_tx):
		return self.transaction_manager.get_transaction_id(_tx)


	#def get_transaction_status(self,_txid):
		#	return self.transaction_manager.get_transaction_status(_txid)


	def get_transaction_status(self,_tx):
		return self.transaction_manager.get_transaction_status(_tx)


	def get_last_transaction(self,_asset_id):
		return self.transaction_manager.get_last_transaction(_asset_id)


	def get_transaction_list(self,_asset_id):
		return self.transaction_manager.get_transaction_list(_asset_id)
	



	#debug methods
	def simulate_mining(self,_tx):
		trials = 0
		print(self.transaction_manager.get_transaction_status(_tx))
		while trials < 60:
		    #print(self.transaction_manager.get_transaction_status(_tx))
		    try:
		        if self.transaction_manager.get_transaction_status(_tx) == 'valid':
		            print('Tx valid in:', trials, 'secs')
		            break
		    except bigchaindb_driver.exceptions.NotFoundError:
		        trials += 1
		        sleep(1)

		if trials == 60:
		    print('Tx is still being processed... Bye!')
		    exit(0)
		#print(self.transaction_manager.get_transaction_status(_tx))
