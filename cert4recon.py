#!/usr/bin/env python3

import requests
import re
import sys
from sys import argv

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'
	INFO = '\033[94m'

def getopts(argv):
	opts = {}  
	while argv:
		try:
			if argv[0][0] == '-':
				opts[argv[0]] = argv[1] 
		except:
			if argv[0] == '-h':
                                print(bcolors.INFO+"[*] "+bcolors.RESET+"usage: ./cert4recon.py [-h] -t target.com [-o output file] [-u up].")
                                sys.exit(0)
		argv = argv[1:] 
	return opts

def main():
	myargs = getopts(argv)
	list=[]
	NoDuplicates_list=[]
	
	url="https://crt.sh/?q="
	
	if len(sys.argv) < 2:
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"No target given.")
		print(bcolors.INFO+"[*] "+bcolors.RESET+"usage: ./cert4recon.py [-h] -t target.com [-o output file].")

	elif '-t' in myargs:
			url = url+myargs['-t']

	regex=r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][-_\.a-zA-Z0-9]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"

	r = requests.get(url)
	jump=r.text.replace("<BR>","\n")
	nohtml=re.sub("<.*?>","",jump)
	nohtml=nohtml.replace(" ","")
	matches = re.finditer(regex, nohtml, re.MULTILINE)

	for matchNum, match in enumerate(matches):

		result= "{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group())
		list.append(result)
	
	for sub in list:
		if sub not in NoDuplicates_list:
			NoDuplicates_list.append(sub)
	
	print("Subdomains found with crt.sh:\n")
	del NoDuplicates_list[0]

	for onlysub in NoDuplicates_list:
		print(bcolors.OK+"[+] "+bcolors.RESET+onlysub)
	
	if '-o' in myargs:
		log = open(myargs['-o'], "w")
		for onlysub in NoDuplicates_list:
			log.write(onlysub+"\n")
		log.close()

	if '-a' in sys.argv:
		print("\n Active HTTP(S) subdomains:\n")
		for onlysub in NoDuplicates_list:
			for proto in ["http://","https://"]:
				try:
					url=proto+onlysub
					rq = requests.get(url)
					print(bcolors.OK+"[+] "+bcolors.RESET+url+bcolors.INFO+" ==> "+bcolors.RESET+rq.url)
				except:
					pass
try:
	main()
except Exception as e:
	print(bcolors.FAIL+"[!] "+bcolors.RESET+"A problem has occured.")
	print(bcolors.FAIL+"[!] "+bcolors.RESET+"No subdomain found.")
	print(bcolors.INFO+"[*] "+bcolors.RESET+"Error info:")
	print(e)
except KeyboardInterrupt:
        print(bcolors.FAIL+"[!] "+bcolors.RESET+"Script canceled.")
