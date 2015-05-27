import json
import sys
import parser
import re

inputfile = open("enronemails.csv", "r")
outputfile = open("orphanemails.csv", "w")
orphanemails={}
print "Gathering orphan emails"

def check_for_orphans(addresses):
	for address in addresses:
		if ("name" in address):
			if (not "email" in address):
				orphanemails[address["name"]] = ''
			elif (address["name"] in orphanemails):
				orphanemails[address["name"]] = address['email']

for line in inputfile.readlines():
	data = line.split("|")
	if (len(data)!=6):
		print "Error! Entry has wrong number of values"
		print line
	date=data[0]
	check_for_orphans(parser.parse_email(data[1]))
	check_for_orphans(parser.parse_email(data[2]))
	check_for_orphans(parser.parse_email(data[3]))
	check_for_orphans(parser.parse_email(data[4]))
inputfile.close()
for orphan in orphanemails.keys():
	if (orphanemails[orphan] == ''):
		orphanemails[orphan] = (".".join(re.findall("[\w]+",orphan)) + "@noemail.com").lower()
	outputfile.write(orphan + "|" + orphanemails[orphan] + "\n")
outputfile.close()
print('Extracted orphan emails')


