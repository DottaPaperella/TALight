#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:34:12 2021

@author: Aurora Rossi

"""

from tabulate import tabulate
import pandas as pd
import copy
import random


def random_quad(q):
    m=random.randrange(3,q)
    n=random.randrange(3,q)
    quad=[['' for j in range(n) ] for i in range(m)]
    for _ in range(len(quad)):
        j=random.randrange(0,len(quad[0])-1)
        i=random.randrange(0,len(quad)-1)
        quad[i][j]='*'
    return quad



def visualizza(quadrante_spaziale):
    index=pd.Index([str(i) for i in range(len(quadrante_spaziale))])
    df=pd.DataFrame(quadrante_spaziale,index=index)
    df = df.iloc[0:,0:]
    columns=["-"]+[str(i) for i in range(len(quadrante_spaziale[0])+10)]
    print(tabulate(df, headers=columns, tablefmt='fancy_grid'))
    
        

def conta_num_met_in(quad):
    num_met=0
    for i in range(len(quad)):
        for j in range(len(quad[0])):
            if quad[i][j]=='*':
                num_met+=1
    return num_met
        
def spara_r(quad,r):
    num_met_destroyed=0
    for j in range(len(quad[0])):
        if quad[r][j]=='*':
            num_met_destroyed+=1
            quad[r][j]='.'
    return num_met_destroyed

def spara_c(quad,c):
    num_met_destroyed=0
    for i in range(len(quad)):    
        if quad[i][c]=='*':
            num_met_destroyed+=1
            quad[i][c]='.'
    return num_met_destroyed
        
def verifica(raggi,quadro_istanza_originale,TAc,LANG):
    quadro_scratch=copy.deepcopy(quadro_istanza_originale)
    num_met_destroyed=0
    for tipo_sparo, pos_sparo in raggi:
        
        if tipo_sparo=='r':
            if pos_sparo < 0 or pos_sparo >= len(quadro_istanza_originale):
                TAc.print(LANG.render_feedback("wrong", f"You shoot on the row {pos_sparo} but the right indeces go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])

    
            num_met_destroyed+=spara_r(quadro_scratch,pos_sparo)
        if tipo_sparo=='c':
            if pos_sparo < 0 or pos_sparo >= len(quadro_istanza_originale[0]):
                TAc.print(LANG.render_feedback("wrong", f"You shoot on the column {pos_sparo} but the right indeces go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])
            num_met_destroyed+=spara_c(quadro_scratch,pos_sparo)
    if conta_num_met_in(quadro_scratch)==0:
        TAc.OK()
        TAc.print(LANG.render_feedback("wrong", "You destroyed all asteroids."), "green", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback("wrong", "You didn't destroyed all asteroids, see what happens."), "red", ["bold"])
        visualizza(quadro_scratch)

            
def presenza_in_rig(asteroidi):
    righe=[]
    for r,c in asteroidi:
        if r not in righe:
            righe.append(r)
        else:
            return True
        
def presenza_in_col(asteroidi):
    col=[]
    for r,c in asteroidi:
        if c not in col:
            col.append(c)
        else:
            return True        
        
def verifica_asteroidi_indipendenti(asteroidi,quadro_istanza_originale,TAc,LANG):
    for i,j in asteroidi:
        if i < 0 or i >= len(quadro_istanza_originale):
            TAc.print(LANG.render_feedback("wrong", f"You shoot on the cell ({i},{j}) but the right row indeces go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])
            return
            
            
        if j < 0 or j >= len(quadro_istanza_originale[0]):
            TAc.print(LANG.render_feedback("wrong", f"You shoot on the cell ({i},{j}) but the right column indeces go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])
            return 
        if quadro_istanza_originale[i][j]!='*':
            TAc.print(LANG.render_feedback("wrong", f"You wrote the cell ({i},{j}) but it doesn't contain asteroids."), "red", ["bold"])
            return 
    if presenza_in_rig(asteroidi):
        TAc.print(LANG.render_feedback("wrong", f"You insert al least two cell of the same row {i}.You can not take more than one cell per row."), "red", ["bold"])
        return 
        
    if presenza_in_col(asteroidi):
        TAc.print(LANG.render_feedback("wrong", f"You insert al least two cell of the same column {j}.You can not take more than one cell per column."), "red", ["bold"])
        return 
    return TAc.print(LANG.render_feedback("right", "Your set is feaseble."), "green", ["bold"])        
    

