from bigchaindb_driver.crypto import generate_keypair

class KeyPair:
	def __init__(self):
		keypair=generate_keypair()
		self.public_key=keypair.public_key
		self.private_key=keypair.private_key