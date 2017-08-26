from pprint import pprint
from time import sleep
from sys import exit
import os





from BlockChainController import BlockChainController












if __name__ == '__main__':
	bdb_driver=BlockChainController('http://0.0.0.0:32769/')
	

	#ESTO NOS LO PASARIA LA APLICACION
	alice, bob, carl = bdb_driver.generate_keypair(),bdb_driver.generate_keypair(),bdb_driver.generate_keypair()
	


	tx=bdb_driver.create_data({'coche': {'matricula': '1111DAD','marca': 'Ferrari', 'modelo':'LaFerrari'}}, {'target-public': 'Bi4 Academy'}, alice.public_key,alice.private_key)
	bdb_driver.simulate_mining(tx)
	

	
	print("ID_ASSET(tx): {}".format(tx['id']))
	asset_id=bdb_driver.search_assets_id("1111DAD")[-1]
	print("ID_ASSET(me): {}".format(asset_id))



	tx2=bdb_driver.create_data({'coche': {'matricula': '1111DAD','marca': 'Ferrari', 'modelo':'LaFerrari'}}, {'target-public': 'PacoLoco'}, alice.public_key,alice.private_key,_asset_id=asset_id)
	bdb_driver.simulate_mining(tx2)



	print("TRANSACCIONES SOBRE EL ASSET:")
	assets_id=bdb_driver.search_assets_id("1111DAD",_unique=False)

	print(assets_id)

	for aid in assets_id:
		print("====================================")
		print(bdb_driver.get_transaction_list(aid))
		print("====================================")




	print("Claves publicas:")
	print("ALICE:")
	print("\tPublica:{}".format(alice.public_key))
	print("\tPrivada:{}".format(alice.private_key))
	print("BOB:")
	print("\tPublica:{}".format(bob.public_key))
	print("\tPrivada:{}".format(bob.private_key))
	




	tx_affected=bdb_driver.transfer_data("1111DAD", alice.public_key,bob.public_key,alice.private_key,_unique=False)
	
	for tx in tx_affected:
		bdb_driver.simulate_mining(tx)
		print("Informacion sobre el asset:{}".format(bdb_driver.get_asset_by_id(tx['asset']['id'])))
		print("Actual propietario: {}".format(bdb_driver.get_ownership(tx['asset']['id'])))
		print("Antiguo propietario: {}".format(bdb_driver.get_previous_owners(tx['asset']['id'])))



	#print("ULTIMA TRANSACCION:")
	#pprint(transaction_manager.get_transaction_list(tx['id'])[-1])





































































































# if __name__ == '__main__':
# 	bdb_driver=BigChainDBDriver('http://0.0.0.0:32768/')
# 	asset_manager=AssetManager(bdb_driver)
# 	transaction_manager=TransactionManager(bdb_driver)


# 	#ESTO NOS LO PASARIA LA APLICACION
# 	alice, bob, carl = KeyPair(), KeyPair(), KeyPair()

# 	asset=Asset({'coche': {'matricula': '1234ABC','marca': 'Ferrari', 'modelo':'LaFerrari'}}, {'target-public': 'Bi4 Academy'})

# 	asset.data['data']['coche']['matricula']="1111CCN"
# 	asset.md['target-public']="Carlos Martinez"

# 	print("===============================")

# 	pprint(asset.data)
# 	pprint(asset.md)


# 	print("===============================")
# 	print("===============================")
# 	print("===============================")






# 	print("\n")

# 	transaction_create=TransactionCreate(alice.public_key,asset)
# 	tx=transaction_manager.direct_process_tx(transaction_create,alice.private_key)

# 	trials = 0
# 	while trials < 60:
# 	    print(transaction_manager.get_transaction_status(tx))
# 	    try:
# 	        if transaction_manager.get_transaction_status(tx) == 'valid':
# 	            print('Tx valid in:', trials, 'secs')
# 	            break
# 	    except bigchaindb_driver.exceptions.NotFoundError:
# 	        trials += 1
# 	        sleep(1)

# 	if trials == 60:
# 	    print('Tx is still being processed... Bye!')
# 	    exit(0)



# 	print(transaction_manager.get_transaction_status(tx))
	

# 	print("ID_ASSET(tx): {}".format(tx['id']))
# 	asset_id=asset_manager.search_asset_id("1111CCN")[-1]
# 	print("ID_ASSET(me): {}".format(asset_id))




# 	asset.md['target-public']="PacoLoco"

# 	transaction_create=TransactionCreate(alice.public_key,asset)
# 	tx2=transaction_manager.direct_process_tx(transaction_create,alice.private_key,asset_id)

# 	trials = 0
# 	while trials < 60:
# 	    print(transaction_manager.get_transaction_status(tx2))
# 	    try:
# 	        if transaction_manager.get_transaction_status(tx2) == 'valid':
# 	            print('Tx valid in:', trials, 'secs')
# 	            break
# 	    except bigchaindb_driver.exceptions.NotFoundError:
# 	        trials += 1
# 	        sleep(1)

# 	if trials == 60:
# 	    print('Tx is still being processed... Bye!')
# 	    exit(0)



# 	print(transaction_manager.get_transaction_status(tx2))







# 	print("TRANSACCIONES SOBRE EL ASSET:")
# 	assets_id=asset_manager.search_asset_id("1111CCN")

# 	print(assets_id)

# 	for aid in assets_id:
# 		print("====================================")
# 		print(transaction_manager.get_transaction_list(aid))
# 		print("====================================")




# 	print("Claves publicas:")
# 	print("ALICE:")
# 	print("\tPublica:{}".format(alice.public_key))
# 	print("\tPrivada:{}".format(alice.private_key))
# 	print("BOB:")
# 	print("\tPublica:{}".format(bob.public_key))
# 	print("\tPrivada:{}".format(bob.private_key))
	






# 	for aid in assets_id:
# 		transaction_transfer=TransactionTransfer(aid,bob.public_key)
# 		tx2=transaction_manager.direct_process_tx(transaction_transfer,alice.private_key,aid)

# 		trials = 0
# 		while trials < 60:
# 		    print(transaction_manager.get_transaction_status(tx2))
# 		    try:
# 		        if transaction_manager.get_transaction_status(tx2) == 'valid':
# 		            print('Tx valid in:', trials, 'secs')
# 		            break
# 		    except bigchaindb_driver.exceptions.NotFoundError:
# 		        trials += 1
# 		        sleep(1)

# 		if trials == 60:
# 		    print('Tx is still being processed... Bye!')
# 		    exit(0)



# 		print(transaction_manager.get_transaction_status(tx2))


# 		print(asset_manager.get_ownership(aid))
# 		print(asset_manager.get_previous_owners(aid))



# 	#print("ULTIMA TRANSACCION:")
# 	#pprint(transaction_manager.get_transaction_list(tx['id'])[-1])






	













