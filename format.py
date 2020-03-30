# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:58:13 2020

@author: romain
"""

import pandas as pd

#On met en forme le planning 
planning = pd.read_csv('planning.txt', header='infer',
                       index_col=['agent','jour','poste'])
planning = planning.unstack(level='poste')
planning = planning.droplevel(level=0, axis=1)
planning.loc[:, 'poste'] = planning.idxmax(axis=1).values
planning.drop(labels=[1,2,3,4,5,6,7], inplace=True, axis=1)
planning = planning.unstack(level='agent')
planning = planning.droplevel(level=0, axis=1)

count_poste = pd.DataFrame(dtype='int64')
for agent in planning.columns:
    count_poste.loc[:, agent] = planning[agent].value_counts()
count_poste.sort_index(inplace=True)
#count_poste.loc[:,[1,2,3,4,5,6,7,8,9]].mean(axis=1)

contraintes = pd.read_csv('contraintes.txt', header='infer',
                          index_col=['agent','contrainte','jour'])
contraintes_semaine = pd.read_csv('contraintes_semaine.txt', header='infer',
                                  index_col=['agent','contrainte','semaine'])

temp = contraintes.droplevel(level=[0,2], axis=0)
count_contraintes_violees = temp.groupby(by='contrainte', axis=0).sum()
temp =\
contraintes_semaine.droplevel(level=[0,2], axis=0).groupby(by='contrainte', axis=0)
count_contraintes_violees = count_contraintes_violees.append(temp.sum())
count_contraintes_violees.sort_values(by='contrainte', inplace=True)

temp = contraintes.droplevel(level=[1,2], axis=0)
count_agents_violees = temp.groupby(by='agent', axis=0).sum()
temp = contraintes_semaine.droplevel(level=[1,2], axis=0).groupby(by='agent', axis=0)
count_agents_violees += temp.sum()

#temp = contraintes.droplevel(level=2, axis=0)
#count_mix_viols = temp.groupby(by=['agent','contrainte'], axis=0).sum()
#count_mix_viols = count_mix_viols.unstack(level='agent')
#count_mix_viols= count_mix_viols.droplevel(level=0, axis=1)
#count_mix_viols.loc[:, 'total'] = count_contraintes_violees.values
#count_mix_viols.loc['total'] = list(count_mix_viols.sum(axis=0).values)