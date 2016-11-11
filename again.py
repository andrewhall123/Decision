from math import log
import pandas as pd
import numpy as np

def divideset(rows,column,value):
	newrows=rows.iterrows()
	split_function=lambda row:row[column]==value
	set1=pd.DataFrame()
	set2=pd.DataFrame()
	for col in range(0,len(rows)):
		if split_function(rows.loc[col]):
			set1=set1.append(rows.loc[col],ignore_index=True)
		else:
			set2=set2.append(rows.loc[col],ignore_index=True)
	return (set1,set2)

def uniquecounts(rows):
	results={}
	for row in range(0,len(rows)):
		r=rows["Play"][row]
		if r not in results:
			results[r]=0
		results[r]+=1
	return results

def entropy(rows):
	log2 = lambda x:log(x)/log(2)
	results=uniquecounts(rows)
	ent=0.0
	for r in results.keys():
		p=results[r]/len(rows)
		ent=ent-p*log2(p)
	return ent

class DecisionNode:
	def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb
		self.fb=fb
		
def buildTree(rows,scoref=entropy):
	if len(rows)==0:
		return DecisionNode()

	current_score=scoref(rows)
	
	best_gain=0.0
	best_set=None
	best_criteria=None
	newrows=list(rows.iterrows())
	for col in rows:
		if col!="Play":
			current_values={}
			for row in newrows:
				current_values[row[1][col]]=1
			for val in current_values:
				(set1,set2)=divideset(rows,col,val)
				p=float(len(set2)/len(rows))
				gain=current_score-p*scoref(set2)-(1-p)*scoref(set1)
			if gain > best_gain and len(set1)>0 and len(set2)>0:
				best_gain=gain
				best_criteria=(col,val)
				print(best_criteria)
				best_set=(set2,set1)
		
	if best_gain>0:
		truebranch=buildTree(best_set[1])
		falsebranch=buildTree(best_set[0])
		return DecisionNode(col=best_criteria[0],value=best_criteria[1],tb=truebranch,fb=falsebranch)
	else:
		print(uniquecounts(rows))
		return DecisionNode(results=uniquecounts(rows))

def printTree(tree,indent=''):
	if tree.results!=None:
		print(str(tree.results))
	else:
		print(str(tree.col)+':', str(tree.value)+'? ')
		print(indent+'T->',end=" ")
		printTree(tree.tb,indent+' ')
		print(indent+'F->',end=" ")
		printTree(tree.fb,indent+' ')

data=pd.read_csv("golf.csv")
rows=data.iterrows()
split_function=lambda row:row[column]==value
#set1,set2=divideset(data,"Play","yes")
#ent=entropy(data)
print(data)
#print(len(list(rows)[0][1]))
tree=buildTree(data)
print(tree.results,type(tree.tb))
printTree(tree)
