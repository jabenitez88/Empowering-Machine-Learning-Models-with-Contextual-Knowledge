# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 23:43:06 2021

@author: MICROSOFT
"""

# %% 


import requests
import json
import pandas as pd
import csv
import time
import re

df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2-classes-entities.csv', sep=';',error_bad_lines=False)

df_1 = df.query("Entities != Classes")

df_1


#%%

df_1

# %% Artificial Intelligence with classes

import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

df_1["Entities"] = df["Entities"].astype('category')
df_1["Classes"] = df["Classes"].astype('category')

df_1["Entities_cat"] = df_1["Entities"].cat.codes
df_1["Classes_cat"] = df_1["Classes"].cat.codes


features = df_1['Entities_cat']
labels = df_1['Classes_cat']

# %%
X = df_1[['Entities_cat','Classes_cat']].copy()


# %%

print(df_1["Entities_cat"].nunique())

# %%

pd.set_option('display.max_rows', None)

pd.set_option('display.max_rows',60)
df2 = df_1.groupby(['Class_labels']).size().sort_values(ascending=False)




# %%

print(df_1.groupby(['Classes_cat']).size().sort_values(ascending=False))

distri_class = df_1.groupby(['Class_labels']).size().sort_values(ascending=False).tolist()

# %%

print(distri_class)

#%%
print('Parent classes of > 10 entities = ', sum(i > 10 for i in distri_class))

print('Parent classes of > 20 entities = ', sum(i > 20 for i in distri_class))

print('Parent classes of > 30 entities = ', sum(i > 30 for i in distri_class))

print('Parent classes of > 40 entities = ', sum(i > 40 for i in distri_class))

print('Parent classes of > 50 entities = ', sum(i > 50 for i in distri_class))

print('Parent classes of > 75 entities = ', sum(i > 75 for i in distri_class))

print('Parent classes of > 100 entities = ', sum(i > 100 for i in distri_class))


# %% 

X_orig = X.copy()

scaler = StandardScaler()
X = scaler.fit_transform(X)

# %%

# Tratamiento de datos
# ==============================================================================
import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot') or plt.style.use('ggplot')

# Preprocesado y modelado
# ==============================================================================
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_score

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')



fig, ax = plt.subplots(1, 1, figsize=(6, 3.84))
ax.scatter(
    x = X[:, 0],
    y = X[:, 1], 
    c = 'white',
    marker    = 'o',
    edgecolor = 'black', 
)
ax.set_title('Datos simulados');

# %% 

X_scaled = X
modelo_kmeans = KMeans(n_clusters=23, n_init=25, random_state=123)
modelo_kmeans.fit(X=X_scaled)

#%%
# Clasificación con el modelo kmeans
# ==============================================================================
y_predict = modelo_kmeans.predict(X=X_scaled)


# %% 

import random

number_of_colors = 1400

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
print(color)

#%%
# Representación gráfica: grupos originales vs clusters creados
# ==============================================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 4))

y = df_1['Classes_cat']

# Grupos originales
'''
for i in np.unique(y):
    ax[0].scatter(
        x = X_scaled[y == i, 0],
        y = X_scaled[y == i, 1], 
        c = plt.rcParams['axes.prop_cycle'].by_key()['color'][i],
        marker    = 'o',
        edgecolor = 'black', 
        label= f"Grupo {i}"
    )
'''
    
#ax[0].set_title('Clusters generados por Kmeans')
#ax[0].legend();

for i in np.unique(y_predict):
    ax.scatter(
        x = X_scaled[y_predict == i, 0],
        y = X_scaled[y_predict == i, 1], 
        c = color[i],
        marker    = 'o',
        edgecolor = 'black', 
        label= f"Cluster {i}"
    )
    
ax.scatter(
    x = modelo_kmeans.cluster_centers_[:, 0],
    y = modelo_kmeans.cluster_centers_[:, 1], 
    c = 'black',
    s = 30,
    marker = '*',
    label  = 'centroides'
)
ax.set_title('Clusters generados por Kmeans')
#ax.legend();