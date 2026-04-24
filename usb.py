import os
import shutil
import time
import argparse
from datetime import datetime
from pathlib import Path
import psutil

CACHE_DIR = "cache_usb"
LOG_FILE = "log.txt"
def detecter_unites_usb():
    lecteurs = []

    for lettre in "DEFGHIJKLMNOPQRSTUVWXYZ":
        chemin = Path(lettre + ":\\")
        if chemin.exists():
            lecteurs.append(str(chemin))

    return lecteurs


def ecrire_log(message):
    date = datetime.now()
    timestamp = date.strftime("%Y-%m-%d %H:%M:%S")
    ligne = "[ " + timestamp + " ] " + message 
    print(ligne)
    try:
        with open(LOG_FILE, "a" ,encoding="utf-8") as fichier:
            fichier.write(ligne + "\n")
    except:
        print("Erreur d'ecriture du fichier de log")



def copier_contenu(source, destination):
    try:
        source_path = Path(source)
        dest_path = Path(destination)

        if not dest_path.exists():
            dest_path.mkdir(parents=True)

        for element in source_path.iterdir():
            try:
                if element.is_file():
                    shutil.copy2(element, dest_path / element.name)

                elif element.is_dir():
                    shutil.copytree(element, dest_path / element.name)

            except Exception:
                continue

    except Exception as e:
        ecrire_log("Erreur lors de la copie : " + str(e))


def nettoyer_lecteur(lecteur):
    try:
        lecteur_path = Path(lecteur)

        for element in lecteur_path.iterdir():
            try:
                if element.is_file():
                    element.unlink()

                elif element.is_dir():
                    shutil.rmtree(element)

            except Exception:
                continue

    except Exception as e:
        ecrire_log("Erreur lors du nettoyage du lecteur : " + str(e))


def initialiser_source(lecteur):
    try:
        ecrire_log("Clé source détectée : " + lecteur)
        if not os.path.exists(CACHE_DIR):
           os.makedirs(CACHE_DIR)
        nettoyer_lecteur(CACHE_DIR)
        ecrire_log("Copie du contenu de la clé source commnencée")
        copier_contenu(lecteur, CACHE_DIR)
        ecrire_log("Copie du contenu de la clé source terminée")
    except Exception as e:
        ecrire_log("Erreur lors de l'initialisation de la source : " + str(e))


def taille_dossier(chemin):
    total = 0
    for racine, dossiers, fichiers in os.walk(chemin):
        for fichier in fichiers:
            chemin_fichier = os.path.join(racine, fichier)
            total += os.path.getsize(chemin_fichier)
    return total

def espace_libre(lecteur):
    total, utilise, libre = shutil.disk_usage(lecteur)
    return libre


def dupliquer_vers_cible(lecteur ,effacer):
    try:

       ecrire_log("Début de la copie vers la clé cible : " + lecteur) 
       taille_cache = taille_dossier(CACHE_DIR)
       libre = espace_libre(lecteur)
       if taille_cache > libre:
          ecrire_log("Espace insuffisant sur la clé cible pour la duplication.")
          return    
       if effacer:
            ecrire_log("Nettoyage de la clé cible avant la duplication.")
            nettoyer_lecteur(lecteur)
       copier_contenu(CACHE_DIR, lecteur)
       #ecrire_log("Duplication vers la clé cible terminée : " + lecteur)
       taille_mo = round(taille_cache / (1024 * 1024), 2)
       ecrire_log("Copie de " + str(taille_mo) + " Mo terminée avec succès.")

    except Exception as e:
        ecrire_log("Erreur lors de la duplication vers la clé cible : " + str(e))
    

# Fonction principale

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--effacer", action="store_true")
    args = parser.parse_args()

    source_initialisee = False
    source_usb = None
    anciennes_cles = []

    message_attente_source = False
    message_attente_cible = False

    ecrire_log("Démarrage du programme...")

    while True:
        cles = detecter_unites_usb()

        # CAS 1 : aucune clé source
        if not source_initialisee:
            if len(cles) > 0:
                source_usb = cles[0]
                initialiser_source(source_usb)
                source_initialisee = True
                message_attente_source = False
            else:
                if not message_attente_source:
                    print("En attente d'une clé USB source...")
                    message_attente_source = True

        # CAS 2 : source déjà définie
        else:
            if not message_attente_cible:
                print("En attente d'une clé USB cible...")
                message_attente_cible = True

            # détecter nouvelles clés
            for cle in cles:
                if cle not in anciennes_cles:
                    ecrire_log("Nouvelle clé cible détectée : " + cle)
                    dupliquer_vers_cible(cle, args.effacer)
                    message_attente_cible = False

            # détecter clés retirées
            for ancienne in anciennes_cles:
                if ancienne not in cles:
                    if ancienne == source_usb:
                        ecrire_log("Clé source débranchée.")
                        source_usb = None  
                    else:
                        ecrire_log("Clé cible débranchée.")

        anciennes_cles = cles.copy()
        time.sleep(3)


if __name__ == "__main__":
    main()