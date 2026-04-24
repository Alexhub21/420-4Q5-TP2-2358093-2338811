from pathlib import Path
from datetime import datetime
import os


class Item:
    def __init__(self, nom, chemin_parent):
        self.nom = nom
        self.chemin_parent = chemin_parent

        self.chemin_complet = Path(chemin_parent) / nom

        if not self.chemin_complet.exists():
            raise FileNotFoundError("Le fichier ou dossier n'existe pas.")

        self.date_creation = datetime.fromtimestamp(self.chemin_complet.stat().st_mtime)

    def ouvrir(self):
        raise NotImplementedError("La méthode ouvrir doit être implémentée dans les classes dérivées.")


class Fichier(Item):
    def __init__(self, nom, chemin_parent):
        super().__init__(nom, chemin_parent)

        self.extension = self.chemin_complet.suffix

    def ouvrir(self):
        if os.name == "nt":
            os.startfile(self.chemin_complet)
        else:
            os.system("xdg-open " + str(self.chemin_complet))


class Dossier(Item):
    def __init__(self, nom, chemin_parent):
        super().__init__(nom, chemin_parent)

    def ouvrir(self):
        if os.name == "nt":
            os.startfile(self.chemin_complet)
        else:
            os.system("xdg-open " + str(self.chemin_complet))

    def retirer_ancien_fichier(self, date):
        for element in self.chemin_complet.iterdir():
            if element.is_file():
                date_modification = datetime.fromtimestamp(element.stat().st_mtime)

                if date_modification < date:
                    element.unlink()