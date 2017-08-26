#from BigChainDBDriver import BigChainDBDriver
from .Asset import Asset

class AssetManager:
	def __init__(self,_bc_driver):
		self.bc_driver=_bc_driver

	def create_asset(self,_asset_dict,_md_dict):
		return Asset({'data': _asset_dict},_md_dict)


	def search_assets(self,_str_criteria,_unique=False):
		assets=self.bc_driver.connection.assets.get(search=_str_criteria)
		if(len(assets)>1 and _unique):
			raise AssertionError('There are more than one assets that matches that criteria. Try changing criteria.')
		elif _unique:
			return assets[0]
		return assets


	def search_asset_id(self,_str_criteria,_unique=False):
		assets=self.bc_driver.connection.assets.get(search=_str_criteria)
		if(len(assets)>1 and _unique):
			raise AssertionError('There are more than one assets that matches that criteria. Try changing criteria.')
		elif _unique:
			return assets[0]['id']

		return [asset['id'] for asset in assets]


	def get_asset_by_id(self,_asset_id):
		return self.bc_driver.connection.transactions.get(asset_id=_asset_id,operation='CREATE')[-1]['asset']


	#def search_asset_metadata(self,_str_criteria,_unique=False):
	#	assets=self.bc_driver.connection.assets.get(search=_str_criteria)
	#	if(len(assets)>1 and _unique):
	#		raise AssertionError('There are more than one assets that matches that criteria. Try changing criteria.')
	#	elif _unique:
	#		return assets[0]['metadata']
	#	return [asset['metadata'] for asset in assets]


	def get_last_transaction(self,_asset_id):
		if(isinstance(_asset_id,list)):
			raise AssertionError('Asset id must be unique, not list.')
		return self.bc_driver.connection.transactions.get(asset_id=_asset_id)[-1]

	def get_ownership(self,_asset_id):
		tx=self.get_last_transaction(_asset_id)
		return tx['outputs'][0]['public_keys'][0]


	def get_previous_owners(self,_asset_id):
		tx=self.get_last_transaction(_asset_id)
		return tx['inputs'][0]['owners_before'][0]
