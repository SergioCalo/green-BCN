#!/usr/bin/env python
# coding: utf-8

# In[9]:


import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pickle

edges = pd.read_csv('graph_sample1.csv')
edges_ruido = pd.read_csv('graph_ruido.csv')
with open('positions.pkl', 'rb') as f:
    positions = pickle.load(f)
    
st.title('Barcelona green routes')


G = nx.Graph()

for i, edge in edges.iterrows():
    G.add_edge(edge['FID_x'], edge['FID_y'], weight=edge['Rang'])


from_node = st.number_input('From node: ', min_value=0, max_value=5000, step=1)
to_node = st.number_input('To node: ', min_value=0, max_value=5000, step=1)

cost_w, path_w = nx.bidirectional_dijkstra(G,from_node,to_node, 'weight')
cost, path = nx.bidirectional_dijkstra(G,from_node,to_node, 1)

st.write('Cost: ', cost_w)
st.write('Nº of edges in the unweighted graph: ', cost)
st.write('Nº of edges in the weighted graph: ', len(path_w))


path_edges = list(zip(path,path[1:]))
path_edges_w = list(zip(path_w,path_w[1:]))

fig, ax = plt.subplots()

nx.draw(G, pos=positions, node_size=20)
nx.draw_networkx_nodes(G,positions,nodelist=path,node_color='r', node_size=30)
nx.draw_networkx_edges(G,positions,edgelist=path_edges,edge_color='r',width=10)

nx.draw_networkx_nodes(G,positions,nodelist=path_w,node_color='g', node_size=30)
nx.draw_networkx_edges(G,positions,edgelist=path_edges_w,edge_color='g',width=10)
fig.set_size_inches(30.5, 30.5)

st.pyplot(fig)





