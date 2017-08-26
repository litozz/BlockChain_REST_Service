from bigchaindb_driver import BigchainDB

class BigChainDBDriver:
	def __init__(self,_root_url):
		self.bdb_root_url=_root_url #Example: 'http://0.0.0.0:32769/'
		self.connection = BigchainDB(self.bdb_root_url)  # this is the driver