class TransactionCreate:
	def __init__(self,_signer_public,_asset):
		self.op_type='CREATE'
		self.signer_public_key=_signer_public
		self.asset=_asset #El asset ya contiene sus metadatos