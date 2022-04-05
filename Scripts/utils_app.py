#!/usr/bin/env python
# coding: utf-8




def stats(G, path, path_w):
    subG = G.subgraph(path)
    print('Normal route: ')
    print('total weight: ', subG.size(weight="weight"))
    print('total noise: ', subG.size(weight="noise"))
    print('total dist: ', subG.size(weight="dist"))
    print('total pollution: ', subG.size(weight="rang"))
    print('')
    subG_w = G.subgraph(path_w)
    print('Green route: ')
    print('total weight: ', subG_w.size(weight="weight"))
    print('total noise: ', subG_w.size(weight="noise"))
    print('total dist: ', subG_w.size(weight="dist"))
    print('total pollution: ', subG_w.size(weight="rang"))
    print('_______________')
    print('Improvement: ')
    print('total weight: ', subG_w.size(weight="weight")/subG.size(weight="weight")*100, '%')
    print('total noise: ', subG_w.size(weight="noise")/subG.size(weight="noise")*100, '%')
    print('total dist: ', subG_w.size(weight="dist")/subG.size(weight="dist")*100, '%')
    print('total pollution: ', subG_w.size(weight="rang")/subG.size(weight="rang")*100, '%')
    imp_w = subG_w.size(weight="weight")/subG.size(weight="weight")*100
    imp_d = subG_w.size(weight="dist")/subG.size(weight="dist")*100
    imp_p =  subG_w.size(weight="rang")/subG.size(weight="rang")*100
    imp_n = subG_w.size(weight="noise")/subG.size(weight="noise")*100
    return imp_w, imp_d, imp_p, imp_n




def stats_alpha(alpha, from_node, to_node, verbose = 1):

    def weight(row, alpha):
        beta = 1 - alpha
        return alpha * row.TOTAL_D + alpha * row.Rang + beta * row.LONGITUD
    edges['weights'] = edges.apply (lambda row: weight(row, alpha), axis=1)
    G = nx.Graph()
    for i, edge in edges.iterrows():
        G.add_edge(edge['FID_x'], edge['FID_y'], noise =  edge['TOTAL_D'], rang = edge['Rang'],  dist = edge['LONGITUD'], weight=edge['weights'])

    path_w = nx.shortest_path(G,from_node,to_node, 'weight')
    path = nx.shortest_path(G,from_node,to_node, 'dist')
        
    subG = G.subgraph(path)
    subG_w = G.subgraph(path_w)
    imp_w = subG_w.size(weight="weight")/subG.size(weight="weight")*100
    imp_d = subG_w.size(weight="dist")/subG.size(weight="dist")*100
    imp_p =  subG_w.size(weight="rang")/subG.size(weight="rang")*100
    imp_n = subG_w.size(weight="noise")/subG.size(weight="noise")*100
    
    if verbose == 1:
        print('Normal route: ')
        print('total weight: ', subG.size(weight="weight"))
        print('total noise: ', subG.size(weight="noise"))
        print('total dist: ', subG.size(weight="dist"))
        print('total pollution: ', subG.size(weight="rang"))
        print('')
        print('Green route: ')
        print('total weight: ', subG_w.size(weight="weight"))
        print('total noise: ', subG_w.size(weight="noise"))
        print('total dist: ', subG_w.size(weight="dist"))
        print('total pollution: ', subG_w.size(weight="rang"))
        print('_______________')
        print('Improvement: ')
        print('total weight: ', subG_w.size(weight="weight")/subG.size(weight="weight")*100, '%')
        print('total noise: ', subG_w.size(weight="noise")/subG.size(weight="noise")*100, '%')
        print('total dist: ', subG_w.size(weight="dist")/subG.size(weight="dist")*100, '%')
        print('total pollution: ', subG_w.size(weight="rang")/subG.size(weight="rang")*100, '%')
    return imp_w, imp_d, imp_p, imp_n

def weight(row, alpha):
    beta = 1 - alpha
    return alpha * row.TOTAL_D + alpha * row.Rang + beta * row.LONGITUD