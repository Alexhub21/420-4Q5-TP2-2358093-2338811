import os
import shutil
import zipfile
import csv
import time
import argparse
import psutil
from datetime import datetime
# dossier de sqauvegarde et historique
DOSSIER_SAUVEGARDE = "Sauvegarde"
FICJIER_LOG = "log.txt"
FICHIER_HISTORIQUE = "historique.csv"
# dossier et fichier si8 non existant
os.makedirs(DOSSIER_SAUVEGARDE, exist_ok=True)
# •	detecter_unites_usb() : Retourne la liste des lecteurs amovibles connectés,
#  en utilisant une librairie externe appropriée par exemple.
def detecter_unites_usb():
    unites_usb = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            unites_usb.append(partition.device)
    return unites_usb
def initialiser_source(lecteur):
    ##

def nettoyer_lecteur(lecteur) :
##
def dupliquer_vers_cible(lecteur) : 
##
