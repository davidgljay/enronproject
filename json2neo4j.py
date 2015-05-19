from py2neo import Graph, Path
import parse_email

graph = Graph('http://davidgljay:clear52@localhost:7474db/data/')
inputfile = open("enronemails.csv", "r")

tx = graph.cypher.begin()
for line in inputfile.readlines():
	data = line.split("|")
	if (len(data)!=6):
		print "Error! Entry has wrong number of values"
		print line
	date=data[0]
	fromval=parse_email.parse_email(data[1])
	to=parse_email.parse_email(data[2])
	cc=parse_email(data[3])
	bcc=parse_email(data[4])
	subject=data[5].rstrip().lstrip().replace('\"','')
	#Replace with neo4j links
	#Create all nodes in from and to
	#Create links with message subject and date
	#Probably best to try in n4j console
	tx.append("MERGE (from:Person" + fromval + ") ")
	# for (i,recipient in to):
	# 		tx.append("MERGE (to" + str(i) + ":Person" + recipient + ") " +
	# 			"CREATE (from)-[:emailed {date:/'" + date + "/', subject:/'" + subject + "/', method:/'to/'}->(to)"
	# output=json.dumps({
	# 	"data":date,
	# 	"from":fromval,
	# 	"to":to,
	# 	"cc":cc,
	# 	"bcc":bcc,
	# 	"subject":subject
	# 	})
tx.commit()
inputfile.close()
#This will require holding the entire thing in memory, it looks like.
#Will it just be easier to put things direclty in from the CSV? Might as well...