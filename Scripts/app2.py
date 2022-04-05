#!/usr/bin/env python
# coding: utf-8



import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import pickle
from utils_app import stats, stats_alpha, weight

edges = pd.read_csv('./data/graph_mix.csv')

with open('./data/positions.pkl', 'rb') as f:
    positions = pickle.load(f)
    
node_features = []
for node in range(max(edges.FID_y)+1):
    result = edges[(edges['FID_x'] == node) | (edges['FID_y'] == node)].Rang
    if len(result)>0:
        node_features.append([node, sum(result)/len(result) ])
        
node_features_pd = pd.DataFrame(node_features, columns=['nodes', 'features'])

st.title('Barcelona green routes')

from_node = st.number_input('From node: ', min_value=0, max_value=9389, step=1)
to_node = st.number_input('To node: ', min_value=0, max_value=9389, step=1)

if from_node == to_node:
    st.write('ATTENTION: The origin and destination must be different!')

alpha = st.slider('Alpha: ', 0.0, 1.0, 0.5, 0.01)

edges['weights'] = edges.apply (lambda row: weight(row, alpha), axis=1)
G = nx.Graph()

for i, node in node_features_pd.iterrows():
    G.add_node(node['nodes'], feature=node['features'])
    
for i, edge in edges.iterrows():
    G.add_edge(edge['FID_x'], edge['FID_y'], noise =  edge['TOTAL_D'], rang = edge['Rang'],  dist = edge['LONGITUD'], weight=edge['weights'])

colors = st.checkbox('Show pollution on map')


if st.button('Run: '):
    path_w = nx.shortest_path(G,from_node,to_node, 'weight')
    path = nx.shortest_path(G,from_node,to_node, 'dist')


    path_edges = list(zip(path,path[1:]))
    path_edges_w = list(zip(path_w,path_w[1:]))
    
    imp_w, imp_d, imp_p, imp_n = stats(G, path, path_w)
    st.write('Improvement: ')
    st.write('total weight: ', imp_w, '%')
    st.write('total noise: ', imp_n, '%')
    st.write('total dist: ', imp_d, '%')
    st.write('total pollution: ', imp_p, '%')

    fig, ax = plt.subplots()
    if colors:
        ec = nx.draw_networkx_edges(G, pos=positions, alpha=0.7)
        nc = nx.draw_networkx_nodes(G, pos=positions,  node_size=20, node_color=node_features_pd.features, cmap=plt.cm.jet)
        plt.colorbar(nc)
    else:
        nx.draw(G, pos=positions, node_size=20)
    nx.draw_networkx_nodes(G,positions,nodelist=path,node_color='r', node_size=30)
    nx.draw_networkx_edges(G,positions,edgelist=path_edges,edge_color='r',width=10)

    nx.draw_networkx_nodes(G,positions,nodelist=path_w,node_color='g', node_size=30)
    nx.draw_networkx_edges(G,positions,edgelist=path_edges_w,edge_color='g',width=10)
    fig.set_size_inches(30.5, 30.5)

    st.pyplot(fig)

    




