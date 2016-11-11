
import os
import subprocess

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz

def get_iris_data():
    """Get the iris data, from local csv or pandas repo."""
    if os.path.exists("iris.csv"):
        print("-- iris.csv found locally")
        df = pd.read_csv("iris.csv", index_col=0)
    else:
        print("-- trying to download from github")
        fn = "https://raw.githubusercontent.com/pydata/pandas/" + \
             "master/pandas/tests/data/iris.csv"
        try:
            df = pd.read_csv(fn)
        except:
            exit("-- Unable to download iris.csv")

        with open("iris.csv", 'w') as f:
            print("-- writing to local iris.csv file")
            df.to_csv(f)

    return df

def encode_target(df, target_column):
	df_mod=df.copy()
	targets=df_mod[target_column].unique()
	map_to_int={name:n for n,name in enumerate(targets)}
	df_mod["Target"]=df_mod[target_column].replace(map_to_int)
	
	return df_mod, targets


def visualize_tree(tree, feature_names):
	with open("dt.dot",'w') as f:
		export_graphviz(tree,out_file=f,feature_names=feature_names)

	command= ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
	try:
		subprocess.check_call(command)
	except:
		exit("Could not run dot, ie graphviz, to "
		     "produce visualization")

df=get_iris_data()

print(df.head(),sep="\n", end="\n\n")
print(df.tail(),sep="\n", end="\n\n")
print("* iris types:", df["Name"].unique(), sep="\n")

df2,targets=encode_target(df,"Name")
print("* df2.head()", df2[["Target", "Name"]].head(),
      sep="\n", end="\n\n")
print("* df2.tail()", df2[["Target", "Name"]].tail(),
      sep="\n", end="\n\n")
print("* targets", targets, sep="\n", end="\n\n")
features = list(df2.columns[:4])
print("* features:", features, sep="\n")


y=df2["Target"]
x=df2[features]
dt=DecisionTreeClassifier(min_samples_split=20,random_state=99)
dt.fit(x,y)



#visualize_tree(dt, features)
