from math import log

def test(data, given):
	

def entropy(attrs,totalDataPoints):
	log2=lambda x: log(x)/log(2)
	totalEntropy=0
	numbers=0
	length=0
	for col in attrs:
		numbers=0
		for val in attrs[col]:
			length=length+val
			numbers+=val
	for col in attrs:
		prob=sum(attrs[col])/totalDataPoints
		ent=0
		if 0 not in attrs[col]:
			for num in attrs[col]:
				ent=ent-((num/sum(attrs[col])*log2(num/sum(attrs[col]))))
			totalEntropy=totalEntropy+(ent*prob)
	return totalEntropy
	
class DecisionNode:
	def __init__(self,col,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb
		self.fb=fb

def buildTree(rows):
	print()


def makeValid(data):
	totalDataPoints=0
	yesnoclass={}
	for point in data:
		pos=0
		neg=0
		yesnoclass[point]=[pos,neg]
		for yesno in data[point]:
			if yesno=="yes":
				totalDataPoints=totalDataPoints+1	
				pos=pos+1
				yesnoclass[point]=[pos,neg]
			elif yesno=="no":
				totalDataPoints=totalDataPoints+1
				neg=neg+1
				yesnoclass[point]=[pos,neg]
		data[point]=[pos,neg]
	return data,totalDataPoints

def splitData(data):
	pos=[]
	neg=[]
	highestEntropy=0
	datasetused=None
	log2=lambda x: log(x)/log(2)
	realentrop=0
	for col in data:
		valid,totaldatapoints=makeValid(data[col])
		ent=lambda x: -(sum(x)/totaldatapoints)*log2(sum(x)/totaldatapoints)
		for i in valid:
			pos.append(valid[i][0])
			neg.append(valid[i][1])
		realentrop=realentrop+ent(pos)+ent(neg)
		realentrop=realentrop-entropy(valid,totaldatapoints)
		if realentrop>highestEntropy:
			highestEntropy=realentrop
			datasetused=col
		pos=[]
		neg=[]
		realentrop=0
	return datasetused

rawdata={"Outlook":{'Sunny':["yes","yes","yes","no","no"],
	  				'Overcast':["yes","yes","yes","yes"],
	  				'Rainy':["yes","yes","no","no","no"]},
	  	 "Temp.":{"Hot":["yes","yes","no","no"],
	  	 		  "Mild":["yes","yes","yes","yes","no","no"],
	  	 		  "Cool":["yes","yes","yes","no"]},
	  	 "Humidity":{"High":["yes","yes","yes","no","no","no","no"],
	  	 			 "Normal":["yes","yes","yes","yes","yes","yes","no"]},
	  	 "Windy":{"False":["yes","yes","yes","yes","yes","yes","no","no"],
	  	 		  "True":["yes","yes","yes","no","no","no"]}}
	  
dataused=splitData(rawdata)
buildTree(rawdata[dataused])
