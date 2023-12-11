from constants import ALLUMETTES_STR, REGLES_STR, JEU_STR
from utils import MessageConsole

def regles() -> None :
    # Ne prends aucun argument
    # Ne renvoie rien, mais affiche les règles du jeu dans le terminal

    print(REGLES_STR)
    print(" - Le jeu se joue à deux joueurs, chacun leur tour, ils doivent retirer 1, 2 ou 3 allumettes")
    print(" - Le joueur qui retire la dernière allumette a perdu\n")
    print(JEU_STR)

def actions(joueur : str, nbAlumettes : int) -> int :
    # Prends en argument le nom du joueur et le nombre d'allumettes restantes
    # Renvoie le nombre d'allumettes restantes après que le joueur ait joué
    
    alumettesSupr : int 

    print(f"\nIl reste {nbAlumettes} allumettes :\n")
    print("▮ "* (nbAlumettes) + "▯ " * (20 - nbAlumettes) + "\n")
    
    alumettesSupr = -1
    while alumettesSupr == -1 :
        alumettesSupr = int(input(f"{joueur}, combien d'allumettes voulez-vous retirer ? [1] [2] [3] \n"))
        if alumettesSupr > 0 and alumettesSupr <= 3 and alumettesSupr <= nbAlumettes :
            nbAlumettes = nbAlumettes - alumettesSupr 
        else :
            print(f"{joueur}, vous ne pouvez pas retirer ce nombre d'allumettes\n")
            alumettesSupr = -1

    return nbAlumettes
    
def Allumettes(joueurs: list[str]) -> list[list[int]]:
    # Prends en argument les deux joueurs qui jouent sous la forme d'une liste de deux str
    # Renvoies une liste de liste de deux entiers représentant l'indice du joueur et le score à ajouter

    nbAlumettes : int
    scoreAAjouter: list[list[int]]

    MessageConsole(ALLUMETTES_STR)
    # On affiche le nom du jeu

    regles()
    # On affiche les règles du jeu


    scoreAAjouter = [[0, 0], [1, 0]]
    # On initialise le score à ajouter pour les deux joueurs

    nbAlumettes = 20
    while nbAlumettes > 0 :
        nbAlumettes = actions(joueurs[0], nbAlumettes)
        if nbAlumettes <= 0 :
            scoreAAjouter[1][1] = 2
        else :
            nbAlumettes = actions(joueurs[1], nbAlumettes)
            if nbAlumettes <= 0 :
                scoreAAjouter[0][1] = 2

    return scoreAAjouter