import sys
print(sys.argv)

import os
print('Get current working directory :      ', os.getcwd())
print('Get current file name :    ', __file__)

print('File name :    ', os.path.basename(__file__))
print('Directory Name:     ', os.path.dirname(__file__))