from py2neo import Graph
import time

queryfile = open("queryfile.txt", "r")
graph = Graph()
i=0;
j=0;
resumepoint = 0
for line in queryfile:
	if resumepoint:
		if i==0:
			tx=graph.cypher.begin()		
		tx.append(line)
		tx.process()
		if i<100:
			i+=1
			j+=1
		elif i>=100:
			tx.commit()
			i=0
			print "Committing transaction " + str(j)
	else:
		if (i>235400):
			resumepoint = 1
			i=0
		else:
			i+=1
print "Donezo"