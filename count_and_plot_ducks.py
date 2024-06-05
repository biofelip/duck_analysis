"""Counts the number of ducks in a set pictures based on csv files generated in picture merger.pu"""
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.cluster.hierarchy import dendrogram, linkage

# load all the the csv files with the results

#root = r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage"
root=r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage"
csvs=glob.glob(os.path.join(root, "**\\drone.csv"))

alldfs=[]
for csv in tqdm(csvs):
    df=pd.read_csv(csv)
    df["xnorm"]=pd.cut(df["longitude"], 5, labels=False)
    df["ynorm"]=pd.cut(df["latitude"], 5, labels=False)
    
    alldfs.append(df)

combined_df=pd.concat(alldfs)

# save as csv

combined_df.to_csv(os.path.join("test.csv"))


# combined the two dataframes
train=pd.read_csv("train.csv")

test=pd.read_csv("test.csv")
df_long=pd.melt(test, id_vars=['date', 'label','latitude','longitude','xnorm', 'ynorm'], 
                value_vars=['Males', 'Females', 'Others'],
                var_name='bird', value_name='count')
df_long.to_csv('long.csv')
rows = []
for _, row in df_long.iterrows():
    for _ in range(row['count']):
        rows.append({
            'date': row['date'],
            'label': row['label'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'xnorm': row['xnorm'],
            'ynorm': row['ynorm'],
            'bird': row['bird'].replace('_count', ''),
        })

df_expanded = pd.DataFrame(rows)
df_expanded.to_csv('expanded.csv')


all_together=pd.concat([train, test])

all_together.to_csv("drone_data_full.csv")

all_together.date.value_counts()

