from py2neo import Graph, Path
import parser
import json

graph = Graph()
inputfile = open("enronemails.csv", "r")

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
	#Replace with neo4j links
	#Create all nodes in from and to
	#Create links with message subject and date
	#Probably best to try in n4j console
	if (len(fromval)>=1):
		query = "MERGE (f"+ str(i) +":Person {name:\"" + fromval[0]["name"] + "\""
		if ("email" in fromval[0]):
			query += ", email:\"" + fromval[0]["email"] + "\""
		query += "}) "
	j=0
	for recipient in to:
		query += "MERGE (t"+ str(i) + "_" + str(j) +":Person {name:\"" + recipient["name"] + "\""
		if ("email" in recipient):
			query += ", email:\"" + recipient["email"] + "\""
		query += "}) "
		query += "CREATE (f" + str(i) + ")-[:emailed {date:\'" + parser.cleantext(date) + "\', subject:\'" + parser.cleantext(subject) + "\', method:\'to\'}]->(t" + str(i) + "_" + str(j) + ") "
		j+=1
	i+=1
	tx.append(query)
tx.commit()
inputfile.close()
#This will require holding the entire thing in memory, it looks like.
#Will it just be easier to put things direclty in from the CSV? Might as well...