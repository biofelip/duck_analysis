import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
from datetime import datetime
df = pd.read_csv('expanded.csv')
df['date']=pd.to_datetime(df['date'],  format='mixed')
#cluster the observations that looks too close to each other and erase them


df["total_ducks"]=df["Males"]+df["Females"]
males=df.pivot_table(index='xnorm', columns='ynorm', values='Males', aggfunc='sum')
females=df.pivot_table(index='xnorm', columns='ynorm', values='Females', aggfunc='sum')
others=df.pivot_table(index='xnorm', columns='ynorm', values='Others', aggfunc='sum')
total_ducks=df.pivot_table(index='xnorm', columns='ynorm', values='total_ducks', aggfunc='sum')


# with exapned dataframe we need to create a contingency table

df['bird'].value_counts()
df_ducks=df[df['bird'] != 'Others']
total_ducks=pd.crosstab( columns=df_ducks['xnorm'], index='count', margins=False)

# before and after the installation of the net 
df_before=df_ducks[df_ducks['date'] < datetime(2023, 11, 13)]
df_after=df_ducks[df_ducks['date'] > datetime(2023, 11, 13)]

total_ducks_before=pd.crosstab(index='count', columns=df_before['xnorm'], margins=False)
total_ducks_before=total_ducks_before.reindex(columns=total_ducks.columns, index=total_ducks.index)
total_ducks_after=pd.crosstab(index='count', columns= df_after['xnorm'], margins=False)
total_ducks_after=total_ducks_after.reindex(columns=total_ducks.columns, index=total_ducks.index)
# Create a colormap with transparency
base_cmap = plt.cm.YlGnBu  # Use any base colormap
transparent_cmap = base_cmap(np.arange(base_cmap.N))
transparent_cmap[:, -1] = 0.7  # Set alpha to 0.5 for 50% transparency
transparent_cmap = mcolors.ListedColormap(transparent_cmap)
def plot_heatmap(df, title=""):
    plt.figure(figsize=(10, 8))
    sn.heatmap(df, annot=True, cmap=transparent_cmap, fmt='.0f', linecolor="white", linewidths=3)
    plt.title(title)
    plt.xlabel('')
    plt.ylabel('')
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    plt.show()


#total ducks
plot_heatmap(total_ducks)
plot_heatmap(total_ducks_before)
plot_heatmap(total_ducks_after)

seasons={'Herbst':[10,11],
         'Winter':[12,1,2],
         'Frühling':[3,4,5]}
# per month
for season in seasons.values():
    try:
        newdf=df_ducks[df_ducks['date'].dt.month.isin(season)]
        newdf['bird'].value_counts()
        crosstab=pd.crosstab(index='count', columns=newdf['xnorm'], margins=False)
        crosstab=crosstab.reindex(columns=total_ducks.columns, index=total_ducks.index)
        key = next(key for key, value in seasons.items() if value == season)
        plot_heatmap(crosstab, title=key)
    except:
        print(f"something wronf with the data at month {key}")
        crosstab

plot_heatmap(total_ducks_before)
plot_heatmap(total_ducks_after)


