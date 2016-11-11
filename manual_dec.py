from sklearn import tree
from sklearn.tree import export_graphviz
import subprocess
import os
import pandas as pd

def visualize_tree(tree, feature_names):
	with open("dt.dot",'w') as f:
		export_graphviz(tree,out_file=f,feature_names=feature_names)

	command= ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
	try:
		subprocess.check_call(command)
	except:
		exit("Could not run dot, ie graphviz, to "
		     "produce visualization")


df=pd.read_csv("voter.csv")
X=[]
Y=[]
x_unseen=[]
y_unseen=[]
count=0
klass=0


rep={'y':0,'n':0}
dem={'y':0,'n':0}

for row in df.values:
	count=count+1
	instvals=[]
	if row[1]=='republican':
		klass=1
	
		"""for yn in row[2:]:
			if yn=='y':
				rep['y']+=1
			elif yn=='n':
				rep['n']+=1"""
	if row[1]=='democrat':
		klass=0
	for vals in row[2:]:
		if vals=='n':
			instvals.append(0)
		if vals=='y':
			instvals.append(1)
	
	if count%2==0:
		y_unseen.append(klass)
		x_unseen.append(instvals)
		
	else:
		Y.append(klass)
		X.append(instvals)
		"""for yn in row[2:]:
			if yn=='y':
				dem['y']+=1
			elif yn=='n':
				dem['n']+=1"""
print(X,"\n\n",Y)

for i in X:
	
