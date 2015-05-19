import json
import sys
import parse_email.parse_email

inputfile = open("enronemails.csv", "r")
outputfile = open("enronemails.json", "w")
outputfile.write('[')
print "Converting from CSV to JSON"

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
