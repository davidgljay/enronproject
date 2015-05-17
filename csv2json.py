import json
import sys
from validate_email import validate_email
import re

inputfile = open("enronemails.csv", "r")
outputfile = open("enronemails.json", "w")
outputfile.write('[')
print "Converting from CSV to JSON"

orphan_addresses={}

def parse_email(entry):
	addresses=[]
	carryover_name = 0
	if (not entry):
		return ''
	address_records = entry.split(",") 
	for address in address_records:
		if (not carryover_name):
			addressinfo = {}
		address.lstrip().rstrip()
		address = re.sub("[\\\"<>\\\']",'',address)
		for item in address.split(" "):
			if (validate_email(item)):
				addressinfo["email"]=item
			elif (re.search('/O=ENRON/OU=NA/CN=RECIPIENTS/CN=',item)):
				item = item.replace('/O=ENRON/OU=NA/CN=RECIPIENTS/CN=', '')
				item = item.lower() + "@enron.com"
				addressinfo["email"]=item
			elif (re.search('\\[mailto\\:', item)):
				item = item.replace('[mailto:', '')
				item = item.replace(']','')
				addressinfo["email"]=item
			elif ("name" in addressinfo):
				addressinfo["name"]+=item + " "
			else:
				addressinfo["name"]=item + " "
		addressinfo["name"] = addressinfo["name"].rstrip().lstrip()
		if (not "email" in addressinfo):
			orphan_addresses[addressinfo["name"]]=''
			carryover_name = 1
			if (address_records[-1] is address):
				addresses.append(addressinfo)
		else:
			if(addressinfo["name"] in orphan_addresses):
				orphan_addresses[addressinfo["name"]] = addressinfo["email"]
			addresses.append(addressinfo)
			carryover_name = 0
	return addresses

lines = inputfile.readlines();
for line in lines:
	data = line.split("|")
	if (len(data)!=6):
		print "Error! Entry has wrong number of values"
		print line
	date=data[0]
	fromval=parse_email(data[1])
	to=parse_email(data[2])
	cc=parse_email(data[3])
	bcc=parse_email(data[4])
	subject=data[5].rstrip().lstrip().replace('\"','')
	output=json.dumps({
		"data":date,
		"from":fromval,
		"to":to,
		"cc":cc,
		"bcc":bcc,
		"subject":subject
		})
	if (not line is lines[-1]):
		output += ",\n"
	outputfile.write(output)
outputfile.write("]")
inputfile.close()
output.close()
print('Writing to JSON file complete')
#Todo: Go through and analyze/clean up orphan addresses.
