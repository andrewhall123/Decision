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

with(open('voter.csv','r')) as f:
	lines=f.readlines()

df=pd.read_csv("voter.csv")

X=[]
Y=[]
x_unseen=[]
y_unseen=[]

count =0
klass=0
for line in lines:
	count=count+1
	values=line.split(',')
	party=values[1]
	
	if 'democrat' in party:
		klass=1
		
	if 'republican' in party:
		klass=0
	
	instanceValues=[]
	for index in enumerate(values,start=1):
		if index[0]==1 or count==1:
			continue
		elif index[0]!=2:
			
			if 'n' in index[1]:
				instanceValues.append(0)
			if 'y' in index[1]:
				instanceValues.append(1)
	
	#Take every other sample and set aside for validation of our decision tree, i.e. don't include these rows in training data
	
	if count%2==0:
		y_unseen.append(klass)
		x_unseen.append(instanceValues)
		
	else:
		Y.append(klass)
		X.append(instanceValues)
		
print ("Total instances:", count)
print ("Training instances:", len(X)-1)
print ("Validation instances:", len(x_unseen))

X=X[1:]
Y=Y[1:]

clf=tree.DecisionTreeClassifier()
clf=clf.fit(X,Y)
predictions=clf.predict(x_unseen)

wrong=0

for index, val in enumerate(predictions):
	if y_unseen[index]!=val:
		wrong=wrong+1
print((len(y_unseen)-wrong)/len(y_unseen))


visualize_tree(clf,df.columns[1:]) 
