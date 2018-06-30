import unittest
import time
import sys
sys.path.append("lib/")
from Contract import *
from bc_admin import *
from ipfs_admin import *
from Developer import *
from User import *

import logging
logging.basicConfig(filename='./logs/example.log',level=logging.DEBUG)

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
ipfs_admin = IPFS_Admin(local = True)
device_t = 1

class TestConnection(unittest.TestCase):
    
    '''
    Test Case 1 (Correct Compilation & Deployment)
    '''
    def test_compile_deploy(self):
        # Initialize and deploy contract
        contract = Contract('contracts/firmware_repo.sol','FirmwareRepo',m_web3,verbose=False)
        tx_hash = contract.publish(blockchain_admin.get_account(0))
        value = contract.get_def_instance().functions.get_version().call()
        self.assertEqual(value,2)

    '''
    Test Case 2 (Basic interaction with contract)
    Set new version Get new version of the Contract
    '''
    def test_basic_interaction(self):
        # Initialize and deploy contract
        contract = Contract('contracts/firmware_repo.sol','FirmwareRepo',m_web3,verbose=False)
        tx_hash = contract.publish(blockchain_admin.get_account(0))
        print("Contract deployed with tx hash: {}".format(tx_hash))
        # Set the contract version to 10
        tx_hash = contract.get_def_instance().functions.set_version(10).transact()
        print("Contract returned: {} value is {}".format(tx_hash,blockchain_admin.get_account(0)))
        #m_web3.eth.waitForTransactionReceipt(tx_hash)
        # Get contract version
        value = contract.get_def_instance().functions.get_version().call()
        print("New contract version {}".format(value))
        self.assertEqual(value,10)

if __name__ == '__main__':
    unittest.main()
