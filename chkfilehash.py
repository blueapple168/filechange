#!/usr/bin/env python
#
# Script to monitor SHA1HASH of file and notify by email if it changes.
# 
# Author : Ketan Patel http://k2patel.in
#
# License : BSD
# Usage : python chkfilehash.py
#
########

import sys
import argparse
import hashlib
import yaml
import os.path

default_file = os.path.expanduser('~')+'/.hash_list'

# Get hash for the file exists.
def gethash1(element, blocksize=65536):
	with open(element, mode='rb') as ofile:
		hash_sha1 = hashlib.sha1()
		while True:
			buf = ofile.read(blocksize)
			if not buf: break
			hash_sha1.update(buf)
		return hash_sha1.hexdigest()

# Update existing configuration
def updateconf(dlist, ofile=default_file):
	with open(ofile, "w") as f:
		yaml.dump(dlist, f, default_flow_style=False)
		f.close

# Create new configuration file if it does not exists.
def setcconf(element, ofile=default_file):
	print("Adding first element " + element + " to configuration.")
	nhash = str(gethash1(element))
	with open(ofile, "w") as f:
		list_doc = {}
		list_doc[str(element)] = nhash
		yaml.dump(list_doc, f, default_flow_style=False)
		f.close

# Add new file to the configuration.
def setelement(existlist, newelement):
	nhash = str(gethash1(newelement))
	existlist[str(element)] = nhash
	return existlist
	
# Read configuration to get old hash for each file specified.
def getcconf(element, cfile=default_file):
    with open(cfile, 'r') as f:
    	cfg = yaml.load(f)
    	f.close
    	if element in cfg:
    		return cfg[element]
    	else:
    		newlist = setelement(cfg, element)
    		updateconf(newlist)
    		return('newelement')

if __name__ == '__main__':
   parser = argparse.ArgumentParser(prog='chkfilehash')
   parser.add_argument('-f', '--file', dest='file', type=str, help='provide full path to the file', nargs='+', required=True)
   #parser.add_argument('-c', '--config', dest='file', type=str, help='provide fulle paht to the file with information, If not provided will create ~/.hash_list', required=False)

   args = parser.parse_args()

   for element in getattr(args, 'file'):
   	if os.path.isfile(default_file):
   		check = getcconf(element)
   		if check is 'newelement':
   			print('New element added to the file : ' + element)
   		else:
   			if check == gethash1(element):
   				print('No change')
   			else:
   				print('change')
   	else:
   		print("Configuration file does not exists we will create new file.")
   		setcconf(element)
