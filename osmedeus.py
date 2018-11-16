#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, glob
import argparse

from core import execute
from core import utils

# import modules 
from modules import subdomain
from modules import takeover
from modules import portscan
from modules import gitscan
from modules import burpstate
from modules import brutethings
from modules import dirbrute

# Console colors
W = '\033[1;0m'   # white 
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G,R,B,P,C,O,GR]


#############
# Osmedeus - One line to rude them all
#############

__author__ = '@j3ssiejjj'
__version__ = '1.0'


### Global stuff
current_path = os.path.dirname(os.path.realpath(__file__))
SPECIAL_ARGUMENT = {
	'TARGET' : 'example.com',
	'STRIP_TARGET' : 'example.com',
	'BURPSTATE' : '',
	'OUTPUT' : 'out.txt',
	'WORKSPACE' : current_path + '/workspaces',

	'PLUGINS_PATH' : current_path + '/plugins',
	'GO_PATH' : '~/go/bin',
	'DIRECTORY_FULL' : '',
	'DOMAIN_FULL' : current_path + '/plugins/wordlists/all.txt',
	'DEFAULT_WORDLIST' : '',

	'GITHUB_API_KEY' : 'db683e65d46c0dc1ba29a5e275c511685b49e17d', # this isn't work api :D 
	'MORE' : '',
	'CWD' : os.path.dirname(os.path.realpath(__file__)),
}
###

options = {
	'target' : '',
	'targetlist' : '',
	'env' : SPECIAL_ARGUMENT,
}


def cowsay():
	print ("""{1}
	  -----------------------------
	< You didn't say the {2}MAGIC WORD{1} >
	  ----------------------------- 
	         \   ^__^
	          \  (oo)\_______
	             (__)\       )\/
	             	\||----w |    
	                 ||     ||    Contact: {2}{3}{1}
		""".format(C, G, P, __author__))


def parsing_argument(args):
	#parsing agument
	if args.git:
		options['env']['TARGET'] = args.git
		# git_routine(options)

	if args.burp:
		options['env']['BURPSTATE'] = args.burp

	if args.more:
		options['env']['MORE'] = args.more

	if args.targetlist:
		options['targetlist'] = args.targetlist
		#check if target list file exist and loop throught the target
		if os.path.exists(options['targetlist']):
			with open(options['targetlist'], 'r+') as ts:
				targetlist = ts.read().splitlines()
			
			for target in targetlist:
				args.target = target
				single_target(args)
				print("{2}>++('> >++('{1}>{2} Target done: {0} {1}<{2}')++< <')++<".format(args.target, P, G))

	else:
		single_target(args)

def single_target(args):
	print('{2}---<---<--{1}@{2} Target: {0} {1}@{2}-->--->---'.format(args.target, P, G))

	if args.target:
		if args.output:
			options['env']['OUTPUT'] = args.output
		else:
			options['env']['OUTPUT'] = args.target

		#just loop in the for if the target list
		options['target'] = args.target
		options['env']['TARGET'] = args.target
		options['env']['STRIP_TARGET'] = args.target.replace('https://','').replace('http://','')
		if '/' in options['env']['STRIP_TARGET']:
			options['env']['STRIP_TARGET'] = options['env']['STRIP_TARGET'].split('/')[0]

		if args.workspace:
			if args.workspace[-1] == '/':
				options['env']['WORKSPACE'] = args.workspace + options['env']['STRIP_TARGET']
			else:
				options['env']['WORKSPACE'] = args.workspace + '/' + options['env']['STRIP_TARGET']
		else:
			options['env']['WORKSPACE'] = current_path + '/workspaces/' + options['env']['STRIP_TARGET']

		#create workspace folder for the target
		initials_stuff(options)

	#run specific task otherwise run the normal routine
	if args.module:
		module = args.module
		if 'subdomain' in module:
			subdomain.SubdomainScanning(options)
			takeover.TakeOverScanning(options)

		elif 'portscan' in module:
			# scanning port, service and vuln with masscan and nmap
			portscan.PortScan(options)

		elif 'git' in module:
			gitscan.GitScan(options)

		elif 'burp' in module:
			burpstate.BurpState(options)

		elif 'brute' in module or 'force' in module:
			# running brute force things based on scanning result
			brutethings.BruteThings(options)

		elif 'dir' in module:
			# run blind directory brute force directly
			dirbrute.DirBrute(options)
			# pass

	else:
		routine(options)


#runnning normal routine if none of module specific
def routine(options):
	#Finding subdomain
	subdomain.SubdomainScanning(options)

	#Scanning for subdomain take over
	takeover.TakeOverScanning(options)

	#Scanning all port using result from subdomain scanning
	portscan.PortScan(options)

	#Brute force service from port scan result
	brutethings.BruteThings(options)

	


#checking the workspace and plugin path
def initials_stuff(options):
	utils.make_directory(options['env']['WORKSPACE'])
	utils.make_directory(options['env']['WORKSPACE'] + '/subdomain')
	utils.make_directory(options['env']['WORKSPACE'] + '/portscan')
	utils.make_directory(options['env']['WORKSPACE'] + '/screenshot')
	utils.make_directory(options['env']['WORKSPACE'] + '/screenshot/all')

	utils.make_directory(options['env']['WORKSPACE'] + '/gitscan/')
	utils.make_directory(options['env']['WORKSPACE'] + '/bruteforce/')
	utils.make_directory(options['env']['WORKSPACE'] + '/directory/')
	utils.make_directory(options['env']['WORKSPACE'] + '/burpstate/')

def list_module():
	print(''' 
List module
===========
subdomain 	- Scanning subdomain and subdomain takerover
portscan 	- Screenshot and Scanning service for list of domain
git 		- Scanning for git repo
burp 		- Scanning for burp state
brute 		- Do brute force on service of target
dirb 		- Do brute force on service of target

		''')
	sys.exit(0)

def update():
	execute.run1('git fetch --all && git reset --hard origin/master && ./install.sh')
	sys.exit(0)

def main():
	cowsay()
	parser = argparse.ArgumentParser(description="Collection tool for automatic pentesting")
	parser.add_argument('-m','--module' , action='store', dest='module', help='specific module to action')
	parser.add_argument('-t','--target' , action='store', dest='target', help='target')
	parser.add_argument('-T','--target_list' , action='store', dest='targetlist', help='list of target')
	parser.add_argument('-o','--output' , action='store', dest='output', help='output')
	parser.add_argument('-b','--burp' , action='store', dest='burp', help='burp http file')
	parser.add_argument('-g','--git' , action='store', dest='git', help='git repo to scan')
	parser.add_argument('-w','--workspace' , action='store', dest='workspace', help='Domain')
	parser.add_argument('--more' , action='store', dest='more', help='append more command for some tools')

	parser.add_argument('-M', '--list_module', action='store_true', help='List all module')
	parser.add_argument('-v', '--verbose', action='store_true', help='show verbose output')
	parser.add_argument('--update', action='store_true', help='update lastest from git')

	args = parser.parse_args()
	if len(sys.argv) == 1:
		# help_message()
		sys.exit(0)

	if args.list_module:
		list_module()
	if args.update:
		update()

	parsing_argument(args)


if __name__ == '__main__':
	main()