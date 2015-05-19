from validate_email import validate_email
import re

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
				addressinfo["email"]=cleantext(item)
			elif (re.search('/O=ENRON/OU=NA/CN=RECIPIENTS/CN=',item)):
				item = item.replace('/O=ENRON/OU=NA/CN=RECIPIENTS/CN=', '')
				item = item.lower() + "@enron.com"
				addressinfo["email"]=item
			elif (re.search('\\[mailto\\:', item)):
				item = item.replace('[mailto:', '')
				item = item.replace(']','')
				addressinfo["email"]=cleantext(item)
			elif ("name" in addressinfo):
				addressinfo["name"]+=cleantext(item) + " "
			else:
				addressinfo["name"]=cleantext(item) + " "
		addressinfo["name"] = addressinfo["name"].rstrip().lstrip()
		if (not "email" in addressinfo):
			# orphan_addresses[addressinfo["name"]]=''
			carryover_name = 1
			if (address_records[-1] is address):
				addresses.append(addressinfo)
		else:
			# if(addressinfo["name"] in orphan_addresses):
				# orphan_addresses[addressinfo["name"]] = addressinfo["email"]
			addresses.append(addressinfo)
			carryover_name = 0
	return addresses

def cleantext(string):
	return re.sub("\'","\\\'", string)