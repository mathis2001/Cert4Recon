#!/usr/bin/env python3

import requests
import re
import sys
from sys import argv
import argparse

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'

def parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", action='store_true', help="target domain(exp: target.com)")
	parser.add_argument("-o", action='store_true', help="Output file name")
	args = parser.parse_args()
	print(args)

def getopts(argv):
	opts = {}  
	while argv:
		if argv[0][0] == '-':
			try:
				opts[argv[0]] = argv[1]  
			except Exception:
				parser()
		argv = argv[1:] 
	return opts

def main():
	myargs = getopts(argv)

	url="https://crt.sh/?q="
	
	if len(sys.argv) < 2:
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"No target given.")

	elif '-t' in myargs:
			url = url+myargs['-t']

	regex=r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][-_\.a-zA-Z0-9]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"

	r = requests.get(url)
	nohtml=re.sub("<.*?>","",r.text)
	nohtml=nohtml.replace(" ","")
	matches = re.finditer(regex, nohtml, re.MULTILINE)

	for matchNum, match in enumerate(matches):

		result= "{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group())
		print(result)
try:
	main()
except Exception as e:
	print(e)
except KeyboardInterrupt:
        print(bcolors.FAIL+"[!] "+bcolors.RESET+"Script canceled.")
