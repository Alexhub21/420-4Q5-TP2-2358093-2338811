from datetime import datetime
from pathlib import Path
from question1 import Fichier, Dossier, Item


# Création de fichiers/dossiers pour tester
Path("test_dossier").mkdir(exist_ok=True)

with open("test.txt", "w", encoding="utf-8") as fichier:
    fichier.write("test")

with open("test_dossier/ancien.txt", "w", encoding="utf-8") as fichier:
    fichier.write("ancien fichier")


print("=== TEST CREATION ===")

fichier = Fichier("test.txt", ".")
dossier = Dossier("test_dossier", ".")

print("Nom fichier :", fichier.nom)
print("Chemin parent :", fichier.chemin_parent)
print("Date création :", fichier.date_creation)
print("Extension :", fichier.extension)

print("Nom dossier :", dossier.nom)
print("Chemin parent :", dossier.chemin_parent)
print("Date création :", dossier.date_creation)


print("\n=== TEST EXCEPTION ===")

try:
    faux = Fichier("inexistant.txt", ".")
except FileNotFoundError as e:
    print("Exception capturée :", e)


print("\n=== TEST METHODE ABSTRAITE ===")

try:
    item = Item("test.txt", ".")
    item.ouvrir()
except NotImplementedError as e:
    print("Exception capturée :", e)


print("\n=== TEST OUVRIR ===")

print("Ouverture du fichier...")
fichier.ouvrir()

print("Ouverture du dossier...")
dossier.ouvrir()


print("\n=== TEST RETIRER ANCIEN FICHIER ===")

date_limite = datetime(2030, 1, 1)
dossier.retirer_ancien_fichier(date_limite)

print("Suppression terminée")