from typing import Optional
import os 

class Joueur :
	nom : str
	robot : bool
	difficulte : Optional[str]
	infoParticulieres: Optional[list[int]]

def MessageConsole(contenu: str):
    # Prends en paramètre une chaine de caractère
	# Supprime le contenu précédent de la console et affiche le nouveau contenu
	# Ne renvoies rien

	# Efface le contenu de la console
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")
		
	print(contenu)