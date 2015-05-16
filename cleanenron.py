from dateutil.parser import *
import re

inputfile = open("sentitems", "r")
outputfile = open("enronemails.csv", "a")
vals={}
for line in inputfile:
	splitline = line.split(":")
	if (splitline[0].lower() == "from"):
		splitline.pop(0)
		vals["from"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "to"):
		splitline.pop(0)
		vals["to"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "cc"):
		splitline.pop(0)
		vals["cc"]=":"join(splitline).rstrip()
	elif (splitline[0].lower() == "bcc"):
		splitline.pop(0)
		vals["bcc"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "date"):
		splitline.pop(0)
		datelist = ":".join(splitline).split(")")
		if (len(datelist)>1):
			datestring = ":".join(splitline).split(")")[0].rstrip().lstrip() + ")"
		else:
			datestring = ":".join(splitline).split(")")[0].rstrip().lstrip()

		print "Date: " + datestring
		vals["date"]=parse(datestring).isoformat()
	elif (splitline[0].lower() == "subject"):
		splitline.pop(0)
		vals["subject"]=":".join(splitline).rstrip().lstrip()
	if ("to" in vals and "from" in vals and "date" in vals and "subject" in vals):
		cc =''
		bcc=''
		if ("cc" in vals):
			cc=vals["cc"]
		if ("bcc" in vals):
			bcc=vals["bcc"]
		outputline = vals["date"] + '|' + vals["from"] + '|' + vals["to"] + '|' + cc + '|' + bcc + '|"' + vals["subject"] + '"\n'
		outputfile.write(outputline)
		vals={}