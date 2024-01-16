from constants import ALLUMETTES_STR, REGLES_STR, JEU_STR
from utils import MessageConsole, Joueur
from random import randint
from statistiques import StatistiqueJeu, GenererFichierCSV
from time import time

def regles() -> None :
    # Ne prends aucun argument
    # Ne renvoie rien, mais affiche les règles du jeu dans le terminal

    print(REGLES_STR)
    print(" - Le jeu se joue à deux joueurs, chacun leur tour, ils doivent retirer 1, 2 ou 3 allumettes")
    print(" - Le joueur qui retire la dernière allumette a perdu\n")
    print(JEU_STR)

def actions(joueur : Joueur, nbAlumettes : int) -> int :
    # Prends en argument le nom du joueur et le nombre d'allumettes restantes
    # Renvoie le nombre d'allumettes restantes après que le joueur ait joué
    
    alumettesSupr : int 

    print(f"\nIl reste {nbAlumettes} allumettes :\n")
    print("▮ "* (nbAlumettes) + "▯ " * (20 - nbAlumettes) + "\n")
    
    alumettesSupr = -1
    if not joueur.robot:
        while alumettesSupr == -1 :
            alumettesSupr = int(input(f"{joueur.nom}, combien d'allumettes voulez-vous retirer ? [1] [2] [3] \n"))
            if alumettesSupr > 0 and alumettesSupr <= 3 and alumettesSupr <= nbAlumettes :
                nbAlumettes = nbAlumettes - alumettesSupr 
            else :
                print(f"{joueur.nom}, vous ne pouvez pas retirer ce nombre d'allumettes\n")
                alumettesSupr = -1
    
    elif joueur.difficulte == "facile":
        
        nbAlumettes = nbAlumettes - randint(1, 3)

    elif joueur.difficulte == "difficile":
        if nbAlumettes % 4 != 1 :
            alumettesSupr = nbAlumettes % 4 - 1
        else :
            if nbAlumettes == 1 :
                alumettesSupr = 1
            elif nbAlumettes <= 4:
                alumettesSupr = nbAlumettes - 1
            else:
                alumettesSupr = 3

    if joueur.robot:
        print(f"{joueur.nom} retire {alumettesSupr} allumettes")

    else :
     nbAlumettes = nbAlumettes - alumettesSupr
    
    return nbAlumettes 

def Allumettes(joueurs: list[Joueur]) -> list[list[int]]:
    # Prends en argument les deux joueurs qui jouent sous la forme d'une liste de deux str
    # Renvoies une liste de liste de deux entiers représentant l'indice du joueur et le score à ajouter

    nbAlumettes : int
    scoreAAjouter: list[list[int]]
    nbManches: list[int]
    listeStatistiques: list[StatistiqueJeu]
    statistique: StatistiqueJeu
    compteurA: int
    tempsA: float
    tempsB: float
    faireStatistiques: str
    joueurQuiCommence: int
    joueurA: int
    joueurB: int

    MessageConsole(ALLUMETTES_STR)
    # On affiche le nom du jeu

    regles()
    # On affiche les règles du jeu

    # On initialise le score à ajouter pour les deux joueurs
    scoreAAjouter = [[0, 0], [1, 0]]
    listeStatistiques = []

    # On initialise la liste des manches
    # La valeur étant le joueuer qui joue en premier
    faireStatistiques = ""
    if joueurs[0].robot and joueurs[1].robot:

        while faireStatistiques != "o" and faireStatistiques != "n":
            faireStatistiques = input("Voulez-vous effectuer des statistiques ? [o/n] ")

        if faireStatistiques == "o":
            nbManches = []
            for compteurA in range(100_000):
                nbManches.append(compteurA % 2)
        else:
            nbManches = [0]

    else:
        nbManches = [0]

    for joueurQuiCommence in nbManches:
        joueurA = joueurQuiCommence
        joueurB = (joueurQuiCommence + 1) % 2
    
        # On génère les statistiques
        statistique = StatistiqueJeu()
        statistique.nomJeu = "Morpion"
        statistique.temps = [[], []]
        statistique.difficultes = []
        statistique.victoire = None
        statistique.valeurParticuliere = None
        if joueurs[0].difficulte and joueurs[1].difficulte:
            statistique.difficultes.append(joueurs[0].difficulte)
            statistique.difficultes.append(joueurs[1].difficulte)

        nbAlumettes = 20
        while nbAlumettes > 0 :

            tempsA = time()
            nbAlumettes = actions(joueurs[joueurA], nbAlumettes)
            tempsB = time()
            statistique.temps[joueurA].append(tempsB - tempsA)

            if nbAlumettes <= 0 :
                scoreAAjouter[1][1] = 2
                statistique.victoire = 1
            else :
                tempsA = time()
                nbAlumettes = actions(joueurs[joueurB], nbAlumettes)
                tempsB = time()
                statistique.temps[joueurB].append(tempsB - tempsA)
                
                if nbAlumettes <= 0 :
                    scoreAAjouter[0][1] = 2
                    statistique.victoire = 0

        if faireStatistiques == "o":
            listeStatistiques.append(statistique)

    if faireStatistiques == "o":
        GenererFichierCSV(listeStatistiques)

    return scoreAAjouter