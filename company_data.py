# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 01:58:04 2020

@author: Harsh
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

company = pd.read_csv("D:\STUDY\Excelr Assignment\Assignment 15 - Random Forests\Company_Data.csv")

##Looking into unique value 
company["Sales"].unique()

company["Sales"].value_counts()
np.median(company["Sales"])

company["sales"]="<=7.49"
company.loc[company["Sales"]>=7.49,"sales"]=">=7.49"

company.drop(["Sales"],axis=1,inplace=True)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
for column_names in company.columns:
    if company[column_names].dtype == object:
        company[column_names]= le.fit_transform(company[column_names])
    else:
        pass
    
featues = company.iloc[:,0:10]
labels = company.iloc[:,10]

##Splitting the data into train and test by using stratify sampling
from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(featues,labels,test_size = 0.3,stratify = labels) 

y_train.value_counts()

y_test.value_counts()

##Building the model
from sklearn.ensemble import RandomForestClassifier as RF

model =RF(n_jobs=4,n_estimators = 150, oob_score =True,criterion ='entropy') 
model.fit(x_train,y_train)
model.oob_score_

##Predicting on training data
pred_train = model.predict(x_train)
##Accuracy on training data
from sklearn.metrics import accuracy_score
accuracy_train = accuracy_score(y_train,pred_train)

##Confusion matrix
from sklearn.metrics import confusion_matrix
con_train = confusion_matrix(y_train,pred_train)

##Prediction on test data
pred_test = model.predict(x_test)

##Accuracy on test data
accuracy_test = accuracy_score(y_test,pred_test)
np.mean(y_test==pred_test)
##Confusion matrix
con_test = confusion_matrix(y_test,pred_test)

##Visualizing the one decision tree in random forest
from sklearn.tree import export_graphviz 
from io import StringIO
import pydotplus
colnames = list(company.columns)
predictors = colnames[0:10]
target = colnames[10]
tree1 = model.estimators_[20]
dot_data = StringIO()
export_graphviz(tree1,out_file = dot_data, feature_names =predictors, class_names = target,
                filled =True,rounded=True, impurity =False,proportion=False,precision =2)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

##Creating pdf file
graph.write_pdf('company_analysis.pdf')

##Creating png file
graph.write_png('company_analysis.png')