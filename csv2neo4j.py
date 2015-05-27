from py2neo import Graph, Path
import parser
import json
import re

graph = Graph()
inputfile = open("enronemails.csv", "r")
orphanemailfile = open("orphanemails.csv","r")
queryfile = open("queryfile.txt","w")

orphanemails = {}
for orphan in orphanemailfile.readlines():
	orphaninfo = orphan.split("|")
	orphanemails[orphaninfo[0]]=orphaninfo[1]
tx = graph.cypher.begin()
i=0
for line in inputfile.readlines():
	data = line.split("|")
	if (len(data)!=6):
		print "Error! Entry has wrong number of values"
		print line
	date=data[0]
	fromval=parser.parse_email(data[1])
	to=parser.parse_email(data[2])
	cc=parser.parse_email(data[3])
	bcc=parser.parse_email(data[4])
	subject=data[5].rstrip().lstrip().replace('\"','')
	for address in fromval:
		if (not "email" in address):
			address["email"]=orphanemails[address["name"]].lstrip().rstrip()
	for address in to:
		if (not "email" in address):
			address["email"]=orphanemails[address["name"]].lstrip().rstrip()
	for address in cc:
		if (not "email" in address):
			address["email"]=orphanemails[address["name"]].lstrip().rstrip()
	for address in bcc:
		if (not "email" in address):
			address["email"]=orphanemails[address["name"]].lstrip().rstrip()

	if (len(fromval)>=1):
		query = "MERGE (f"+ str(i) +":Person {email:\"" + fromval[0]["email"] + "\"}) "
		if ("name" in fromval[0]):
			query +="ON CREATE SET f"+ str(i) + " += {name:\"" + fromval[0]["name"] + "\"} "
	j=0
	for recipient in to:
		query += "MERGE (t"+ str(i) + "_" + str(j) +":Person {email:\"" + recipient["email"] + "\"}) "
		if ("name" in recipient):
			query +="ON CREATE SET t"+ str(i) + "_" + str(j) + " += {name:\"" + recipient["name"] + "\"} "
		query += "CREATE (f" + str(i) + ")-[:emailed {date:\'" + parser.cleantext(date) + "\', subject:\'" + parser.cleantext(subject) + "\', method:\'to\'}]->(t" + str(i) + "_" + str(j) + ") "
		j+=1
	for recipient in cc:
		query += "MERGE (cc"+ str(i) + "_" + str(j) +":Person {email:\"" + recipient["email"] + "\"}) "
		if ("name" in recipient):
			query +="ON CREATE SET cc"+ str(i) + "_" + str(j) + " += {name:\"" + recipient["name"] + "\"} "
		query += "CREATE (f" + str(i) + ")-[:emailed {date:\'" + parser.cleantext(date) + "\', subject:\'" + parser.cleantext(subject) + "\', method:\'cc\'}]->(cc" + str(i) + "_" + str(j) + ") "
		j+=1
	for recipient in bcc:
		query += "MERGE (bcc"+ str(i) + "_" + str(j) +":Person {email:\"" + recipient["email"] + "\"}) "
		if ("name" in recipient):
			query +="ON CREATE SET bcc"+ str(i) + "_" + str(j) + " += {name:\"" + recipient["name"] + "\"} "
		query += "CREATE (f" + str(i) + ")-[:emailed {date:\'" + parser.cleantext(date) + "\', subject:\'" + parser.cleantext(subject) + "\', method:\'bcc\'}]->(bcc" + str(i) + "_" + str(j) + ") "
		j+=1

	query = query.encode("utf-8")
	queryfile.write(query + "\n")
	# tx.append(query)
	# tx.process()
	i+=1
# tx.commit()

queryfile.close()
inputfile.close()
orphanemailfile.close()

