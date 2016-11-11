from sklearn.tree import DecisionTreeClassifier,export_graphviz
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.externals.six import StringIO

def get_data():
	df=pd.read_csv('golf.csv')
	return df
	
"""def encode_target(df,target_col):
	df_mod=df.copy()
	targets=df_mod[target_col].unique()
	map_to_int={name:n for n,name in enumerate(targets)}
	df_mod["Targets"]=df_mod[target_col].replace(map_to_int)
	
	return (df_mod,targets)	
	
df=get_data()
print(encode_target(df,"Play"))"""

def format(data,declare):
	for param in declare:
			data=data.replace(True,1)
			data=data.replace(False,0)
			data=data.replace(param,declare[param])
	
	return data

train_df=get_data()
print(train_df)
train_df.Windy=train_df.Windy.astype(int)
train_df=format(train_df,{'sunny':2,'overcast':1,'rainy':0,'hot':2,'mild':1,'cool':0,
							   'normal':0,'high':1,'False':0,'True':1,'no':0,'yes':1})
print(train_df)

Y=targets=labels=train_df['Play'].values

columns=[col for col in train_df.columns if col!="Play"]
features=train_df[list(columns)].values

imp=Imputer(missing_values="NaN",strategy='mean',axis=0)
X=imp.fit_transform(features)
print(X)
clf=DecisionTreeClassifier(criterion="entropy",max_depth=3)
clf.fit(X,Y)

print(clf.predict([[2,2,2,0]]))



with open("real.dot", 'w') as f:
  f = export_graphviz(clf, out_file=f, feature_names=columns)




