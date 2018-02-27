
import pandas as pd
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

#reading the csv
data = pd.read_csv('F:/Sample_Input.csv')

#creates a map between the conversion of string and its factor conversion .
def mapping_function(column):
    unique = pd.unique(column)
    unique_df = pd.DataFrame(unique)
    map_df = pd.Categorical.from_array(unique).labels
    unique_df['maps'] = map_df
    return unique_df

maps = {}

for cols in data.columns :
    maps[cols] = mapping_function(data[cols])

#changes a string to factor according to mapping function created .
def factor_function(k,cols):
    df = np.array(maps[cols])
    for d,f in df :
        if(d == k):
            return(f)
        
#changes a factor back to string according to mapping function created .
def defactor_function(k,cols):
    df = np.array(maps[cols])
    for d,f in df :
        if(f == k):
            return(d)
        
            
for cols in data.columns :
    for i in range(0,len(data)):
        data[cols][i] = factor_function(data[cols][i],cols)
        

#calculation of sum squared error for different number of clusters.        
sse = {}
for k in range(1,11):
    sse[k] = 0 
    kmeans = cluster.k_means(data,k)
    ndata = data
    ndata['cluster'] = kmeans[1]
    for i in range(0,k):
        temp = ndata.where(ndata['cluster']==i)
        sse[k] = sse[k] + sum((temp.loc[:,'ln'].dropna() - kmeans[0][i][0])*(temp.loc[:,'ln'].dropna() - kmeans[0][i][0]))+ sum((temp.loc[:,'dob'].dropna() - kmeans[0][i][1])*(temp.loc[:,'dob'].dropna() - kmeans[0][i][1]))+ sum((temp.loc[:,'gn'].dropna() - kmeans[0][i][2])*(temp.loc[:,'gn'].dropna() - kmeans[0][i][2]))+ sum((temp.loc[:,'fn'].dropna() - kmeans[0][i][3])*(temp.loc[:,'fn'].dropna() - kmeans[0][i][3]))


#plotting the skee plot .
plt.plot(sse.keys(),sse.values())

fdata = data.loc[:,'ln':'fn']

#Clusters selected according to the skee plot.
clusters = 3

final_cluster = cluster.k_means(fdata,clusters)

for cols in fdata.columns :
    for i in range(0,len(fdata)):
        fdata[cols][i] = defactor_function(fdata[cols][i],cols)

fdata['cluster'] = final_cluster[1]

#Calculation of score between two strings .
def score_function(s1,s2):
    dist = fuzz.ratio(s1,s2)
    return dist


#Calculation of Score matrix and selection of unique records.
for k in range(0,clusters) :
    cdata = fdata.where(fdata['cluster']==k)
    cdata = cdata.loc[:,'ln':'fn']
    cdata = cdata.dropna()
    ndata = cdata
    scores = pd.DataFrame(index = cdata.index,columns = cdata.index)
    for i in cdata.index:
        for j in cdata.index:
            if(i!=j):
                scores[i][j] =  (2*score_function(cdata['ln'][i],cdata['ln'][j]) + score_function(cdata['dob'][i],cdata['dob'][j]) + score_function(cdata['gn'][i],cdata['gn'][j]) + 2*score_function(cdata['fn'][i],cdata['fn'][j]))/6

    for i in cdata.index:
        if(i in ndata.index) :
            del_index = scores.loc[i,:].where(scores.loc[i,:]>95).dropna().index
            if( len(del_index)!=0 ):
                ndata = ndata.drop(del_index)
    
    if(k==0):
        final = ndata
    if(k!=0):
        final = final.append(ndata)
            
        
#Saiving of output .        
writer = pd.ExcelWriter('F:/output.xlsx')
final.to_excel(writer)















