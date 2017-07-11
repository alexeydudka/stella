#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Main module of stella system

import sys,os

# Loading stella system libraries
try:
	import st_parser
except Exception as e:
	print("Status: 500 Internal Server Error")
	print("Content-Type: text/html\n\n")
	print("Error: "+str(e))
	sys.exit(1)

if 'PATH_TRANSLATED' in os.environ:
	script=os.environ['PATH_TRANSLATED']
	if 'REDIRECT_VIRTUAL' in os.environ:
		os.environ['DOCUMENT_ROOT'] = os.environ['PATH_TRANSLATED'][0:-len(os.environ['REDIRECT_URL'])]
else:
	print("Status: 500 Internal Server Error")
	print("Content-Type: text/html\n\n")
	print("Error: I don't get script name from env='PATH_TRANSLATED'.")
	sys.exit(1)

try:
	st_parser.do(script)
except Exception as e:
	print("Status: 500 Internal Server Error")
	print("Content-Type: text/html\n\n")
	print("Error: "+str(e))
	sys.exit(1)