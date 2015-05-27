from dateutil.parser import *
import re
import sys

if (len(sys.argv)<1 or len(sys.argv)>2):
	print "You must enter exactly one file to scan for email."
	sys.exit()
else:
	ifile = sys.argv[1]
counter = 0
inputfile = open(ifile, "r")
outputfile = open("enronemails.csv", "a")

print "Scanning " + ifile

vals={}
for line in inputfile:
	splitline = line.split(":")
	if (splitline[0].lower() == "from" and not "from" in vals):
		splitline.pop(0)
		vals["from"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "to" and not "to" in vals):
		splitline.pop(0)
		vals["to"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "cc" and not "cc" in vals):
		splitline.pop(0)
		vals["cc"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "bcc" and not "bcc" in vals):
		splitline.pop(0)
		vals["bcc"]=":".join(splitline).rstrip()
	elif (splitline[0].lower() == "date" and not "date" in vals):
		splitline.pop(0)
		datelist = ":".join(splitline).split(")")
		if (len(datelist)>1):
			datestring = ":".join(splitline).split(")")[0].rstrip().lstrip() + ")"
		else:
			datestring = ":".join(splitline).split(")")[0].rstrip().lstrip()
		vals["date"]=parse(datestring).isoformat()
	elif (splitline[0].lower() == "subject" and not "subject" in vals):
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
		counter+=1
print "Added " + str(counter) + " emails to enronemails.csv"
