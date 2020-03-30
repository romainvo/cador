# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 10:38:44 2020

@author: romain
"""

import pandas as pd

#-------------------------------------------------------------------------------
#------------------------ CALCUL ETP REQUIS ANNEE 2020 -------------------------
#-------------------------------------------------------------------------------

besoins = [[2,1,1,2],
          [2,1,1,2],
          [2,1,1,2],
          [2,1,1,2],
          [2,1,1,2],
          [2,1,0,2],
          [2,1,0,2]]

besoins = pd.DataFrame(besoins)
besoins.index = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
besoins.columns = ['matin','jour','soir','nuit']

nombre_jours = {'lundi':52,'mardi':52,'mercredi':53,'jeudi':53,'vendredi':52,
                'samedi':52,'dimanche':52}
jours_feries = {'lundi':2,'mardi':1,'mercredi':2,'jeudi':1,'vendredi':3,'samedi':1,'dimanche':1}
duree_poste = {'matin':7.5,'jour':7.5,'soir':7.5,'nuit':10}

heures_annuelles = [[1575, 1545],
                    [1466, 1452]]
heures_annuelles = pd.DataFrame(heures_annuelles)
heures_annuelles.columns = ['fixe', 'variable']
heures_annuelles.index = ['jour', 'nuit']

ETPR_jour = 0
for poste in besoins.columns:
    if poste != 'nuit':
        for jour in nombre_jours.keys():
            ETPR_jour += besoins.loc[jour,poste] * nombre_jours[jour] * duree_poste[poste]
ETPR_jour /= heures_annuelles.loc['jour','fixe']

ETPR_nuit = 0
for jour in nombre_jours.keys():
    ETPR_nuit += besoins.loc[jour,'nuit'] * nombre_jours[jour] * duree_poste['nuit']
ETPR_nuit /= heures_annuelles.loc['nuit','fixe']

NbDF_jour = 0
for poste in besoins.columns:
    if poste != 'nuit':
        NbDF_jour += besoins.loc['dimanche',poste] * nombre_jours['dimanche']
for poste in besoins.columns:
    if poste != 'nuit':
        for jour_ferie in jours_feries.keys():
            if jour_ferie != 'dimanche':
                NbDF_jour += besoins.loc[jour_ferie, poste] * jours_feries[jour_ferie]

NbDF_nuit = 0
NbDF_nuit += besoins.loc['dimanche','nuit'] * nombre_jours['dimanche']
for jour_ferie in jours_feries.keys():
    if jour_ferie != 'dimanche':
        NbDF_nuit += besoins.loc[jour_ferie, 'nuit'] * jours_feries[jour_ferie]
    
NbDF = (NbDF_jour + NbDF_nuit) / (ETPR_jour + ETPR_nuit) 

if NbDF > 10:
    ETPR_jour = 0
    for poste in besoins.columns:
        if poste != 'nuit':
            for jour in nombre_jours.keys():
                ETPR_jour += besoins.loc[jour,poste] * nombre_jours[jour] * duree_poste[poste]
    ETPR_jour /= heures_annuelles.loc['jour','variable']
    
    ETPR_nuit = 0
    for jour in nombre_jours.keys():
        ETPR_nuit += besoins.loc[jour,'nuit'] * nombre_jours[jour] * duree_poste['nuit']
    ETPR_nuit /= heures_annuelles.loc['nuit','variable']    

ETPR = ETPR_jour + ETPR_nuit
if ETPR < 2 * besoins.loc['dimanche'].sum():
    ETPR = 2 * besoins.loc['dimanche'].sum() 