from validate_email import validate_email
import re

def parse_email(entry):
	addresses=[]
	carryover_name = 0
	if (not entry):
		return ''
	if (len(re.findall(";",entry))>0):
		address_records = re.split("[;]",entry)
	elif (len(re.findall("[\w]+",entry))>3):
		address_records = re.split("[\\,]",entry)
	else:
		address_records = [entry]
	for address in address_records:
		addressinfo = {}
		address.lstrip().rstrip()
		address = address.split(" on ")[0]
		# Clean extraneous strings.
		address = address.replace("@ENRON", '')
		address = address.replace("@ ENRON", '')
		address = address.replace("(E-mail)", '')
		address = address.replace("\(E-mail\)", '')
		address = address.replace("\(E-mail\)", '')
		address = re.sub("[\\\"<>\\\'\\\\:]",'',address)
		for item in address.split(" "):
			if (validate_email(item)):
				addressinfo["email"]=cleantext(item).rstrip().lstrip().lower()
			elif (re.search('/O=ENRON/OU=NA/CN=RECIPIENTS/CN=',item)):
				item = item.replace('/O=ENRON/OU=NA/CN=RECIPIENTS/CN=', '')
				item = item.lower() + "@enron.com"
				addressinfo["email"]=item.rstrip().lstrip().lower()
			elif (re.search('\\[mailto\\:', item)):
				item = item.replace('[mailto:', '')
				item = item.replace(']','')
				addressinfo["email"]=cleantext(item).rstrip().lstrip().lower()
			elif ("name" in addressinfo):
				addressinfo["name"]+=cleantext(item) + " "
			else:
				addressinfo["name"]=cleantext(item) + " "
		if ("name" in addressinfo):
			addressinfo["name"] = addressinfo["name"].rstrip().lstrip()
		addresses.append(addressinfo)
	return addresses

def cleantext(string):
	string = string.replace("//","////")
	# \\,\\.\\/\\!@#$%\\^\\&*()\\-\\+\\|\\[\\]}{ _\\:;\'\"<>
	funkychars = "[^a-zA-Z0-9\,\.\/\\!@#\$\?%\^\&\*\(\)\-\+\|\[\]\}\{= _:;\'\"\<\>]"
	if (len(re.findall( funkychars,string)) > 0):
		print re.findall(funkychars,string)
		string = re.sub(funkychars, " ",string)
	return string.encode("string_escape")