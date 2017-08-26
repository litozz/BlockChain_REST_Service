class TransactionTransfer:
	def __init__(self,_asset_id,_recipients):
		self.op_type='TRANSFER'
		self.asset={'id': _asset_id}
		self.inputs=None
		self.recipients=_recipients