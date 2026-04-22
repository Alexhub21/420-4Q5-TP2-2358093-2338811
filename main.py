from datetime import datetime, timedelta
from question1 import Fichier, Dossier

if __name__ == "__main__":
    # Création d'un fichier et d'un dossier existants
    try:
        fichier = Fichier("question1.txt", ".", datetime.now(), "py")
        print("Fichier créé avec succès.")
        fichier.ouvrir()  # Ouvre le fichier avec l'éditeur par défaut
        
        dossier = Dossier("Tp2", "..", datetime.now())
        print("Dossier créé avec succès.")
        dossier.ouvrir()  # Ouvre le dossier dans l'explorateur
        
        # Tester retirer_ancien_fichier avec une date passée
        old_date = datetime.now() - timedelta(days=1)
        dossier.retirer_ancien_fichier(old_date)
        print("Anciens fichiers supprimés.")
        
    except FileNotFoundError as e:
        print(f"Erreur : {e}")
    
    # Tester l'exception pour un fichier inexistant
    try:
        fichier_inexistant = Fichier("inexistant.txt", ".", datetime.now(), "txt")
    except FileNotFoundError as e:
        print(f"Exception levée pour fichier inexistant : {e}")
    
    # Tester l'exception pour un dossier inexistant
    try:
        dossier_inexistant = Dossier("Inexistant", ".", datetime.now())
    except FileNotFoundError as e:
        print(f"Exception levée pour dossier inexistant : {e}")
        print("Fichier et dossier créés avec succès.")
    except FileNotFoundError as e:
        print(e)

    # Test de l'exception pour un fichier inexistant
    try:
        fichier_inexistant = Fichier("inexistant.txt", "C:/Users/Utilisateur/Documents", datetime.now(), "txt")
    except FileNotFoundError as e:
        print(e)

    # Test de l'exception pour un dossier inexistant
    try:
        dossier_inexistant = Dossier("InexistantDossier", "C:/Users/Utilisateur/Documents", datetime.now())
    except FileNotFoundError as e:
        print(e)

    # Test de la méthode ouvrir()
    try:
        fichier.ouvrir()
        dossier.ouvrir()
        print("Fichier et dossier ouverts avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ouverture : {e}")

    # Test de la méthode retirer_ancien_fichier()
    try:
        date_limite = datetime.now() - timedelta(days=30)  # Supprimer les fichiers modifiés il y a plus de 30 jours
        dossier.retirer_ancien_fichier(date_limite)
        print("Fichiers anciens retirés avec succès.")
    except Exception as e:
        print(f"Erreur lors du retrait des anciens fichiers : {e}")
