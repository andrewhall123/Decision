import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import os
import subprocess
from sklearn.cross_validation import train_test_split

def get_data():
    """Get the iris data, from local csv or pandas repo."""
    if os.path.exists("votes.csv"):
        print("-- iris.csv found locally")
        df = pd.read_csv("votes.csv", index_col=0)
    else:
        print("-- trying to download from github")
        fn = "https://archive.ics.uci.edu/ml/machine-learning-databases/voting-records/house-votes-84.data"
        try:
            df = pd.read_csv(fn)
        except:
            exit("-- Unable to download iris.csv")

        with open("votes.csv", 'w') as f:
            print("-- writing to local iris.csv file")
            df.to_csv(f, sep=',', na_rep='?')
    df.dropna()
    return df
    
data=get_data()


for j,column in enumerate(data.values):
	if '?' in column:
		data=data.drop([j])

data.columns=['Class Name', 'handi','water','adopt', 'phys','el','rel','anti','aid','mx','immi','synfuel','edu','super','crime','duty', 'export']

data.replace(to_replace='y',value=1,inplace=True)
data.replace(to_replace='n',value=0,inplace=True)
data.replace(to_replace='democrat',value=1,inplace=True)
data.replace(to_replace='republican',value=0,inplace=True)

print(data)

xunseen=[]
yunseen=[]

for i in data.values:
	for j in i:
		print(j)

train, test=train_test_split(data, test_size=0.5)



X = [[0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0], [0,1,1,0,1,1,1,1,0,0,1,0,1,0,1,1]]

Y=[0,1]

clf=DecisionTreeClassifier()
clf=clf.fit(X,Y)

train=train.columns[1:]
train=train.values[1:]
print(train[1:])
#predictions=clf.predict(train)

