from constants import DEVINETTE_STR, REGLES_STR, JEU_STR
from utils import MessageConsole, Joueur
from random import randint
from statistiques import StatistiqueJeu, GenererFichierCSV
from typing import Optional
from time import time

def regles() -> None :
    # Ne prends aucun argument
    # Ne renvoie rien, mais affiche les règles du jeu dans le terminal

    print(REGLES_STR)
    print(" - Le premier joueur doit choisir un nombre entre 1 et un nombre maximum")
    print(" - Le second joueur doit deviner le nombre choisi par le premier joueur")
    print(JEU_STR)

def DemanderNombre(joueur: Joueur, nombreMax: int) -> int :
    # Prends en argument le nom du joueur qui doit deviner le nombre
    # Et l'intervalle maximal dans lequel le nombre peut être choisi

    nombreSelect : int


    # On demande au joueur de choisir un nombre
    nombreSelect = -1

    if not joueur.robot:
        while nombreSelect <= 0 or nombreSelect > nombreMax :
            nombreSelect = int(input(f"\n{joueur.nom}: Proposez un nombre entre 1 et {nombreMax} : \n"))

            if nombreSelect <= 0 or nombreSelect > nombreMax :
                print(f"Le nombre choisi doit être compris entre 1 et {nombreMax}")
    else:
        nombreSelect = randint(1, nombreMax)

    return nombreSelect

def DemanderReponse(joueurs: list[Joueur], nombreSelect: int, nombreCible: int, scores: list[list[int]]) -> None :
    # Prends en argument une liste de deux chaines de caractères représentant les noms des joueurs
    # Et le nombre choisi par le joueur ainsi que celui qui doit le deviner
    # Ne renvoies rien, mais envoie dans le terminal la réponse du joueur

    reponseSelect: int
    demandeEnCours : bool
    
    # On demande au joueur de choisir une réponse
    demandeEnCours = True

    MessageConsole("\n")
    print(f"\n{joueurs[1].nom} propose le nombre : {nombreSelect}")
    print(f"Le nombre à deviner est : {nombreCible}")
    print(f"\n{joueurs[0].nom}: Sélectionnez une réponse parmis :")
    print("1. Le nombre à deviner est plus grand")
    print("2. Le nombre à deviner est plus petit")
    print("3. Vous avez gagné ! \n")
    
    if not joueurs[0].robot:
        while demandeEnCours :
            reponseSelect = int(input())
            if reponseSelect <= 0 or reponseSelect > 3 :
                print("La réponse doit être comprise entre 1 et 3")

            if reponseSelect == 1 :
                if nombreSelect >= nombreCible :
                    print("Bien tenté mais non, faut pas tricher, réessayez")
                    scores[0][1] = scores[0][1]-1

                else :
                    MessageConsole(f"{joueurs[0].nom}: Le nombre est plus grand")
                    scores[0][1] = scores[0][1]+1
                    demandeEnCours = False

            elif reponseSelect == 2 :
                if nombreSelect <= nombreCible :
                    print("Bien tenté mais non, faut pas tricher, réessayez")
                    scores[0][1] = scores[0][1]-1

                else :
                    MessageConsole(f"{joueurs[0].nom}: Le nombre est plus petit")
                    scores[0][1] = scores[0][1]+1
                    demandeEnCours = False

            elif reponseSelect == 3 :
                if nombreSelect == nombreCible :
                    MessageConsole(f"{joueurs[0].nom}: Bravo {joueurs[1].nom} tu as gagné")
                    scores[0][1] = scores[0][1]+1
                    demandeEnCours = False

                else :
                    print("Bien tenté mais non, faut pas tricher, réessayez")
                    scores[0][1] = scores[0][1]-1
        scores[1][1] = scores[1][1]-1
    else:
        if nombreSelect > nombreCible:
            MessageConsole(f"{joueurs[0].nom}: Le nombre est plus grand")
            scores[0][1] = scores[0][1]+1

        elif nombreSelect < nombreCible:
            MessageConsole(f"{joueurs[0].nom}: Le nombre est plus petit")
            scores[0][1] = scores[0][1]+1

        elif nombreSelect == nombreCible:
            MessageConsole(f"{joueurs[0].nom}: Bravo {joueurs[1].nom} tu as gagné")
            scores[0][1] = scores[0][1]+1

        scores[1][1] = scores[1][1]-1
                

def Devinette(joueurs: list[Joueur]) -> list[list[int]]:
    # Prends en argument une liste de deux chaines de caractères représentant les noms des joueurs
    # Le premier joueur étant celui qui doit demander le nombre
    # Et le second celui qui doit deviner le nombre
    # Renvoies une liste de liste de deux entiers représentant l'indice du joueur et le score à ajouter

    nombreCible : int
    nombreSelect : int
    nombreMax : int
    jeuEnCours : bool
    scores: list[list[int]]
    listStatistiques: list[StatistiqueJeu]
    statistique: StatistiqueJeu
    listeNbMax: list[Optional[int]]
    nbMaxListe: Optional[int]    
    compteur: int
    listeJoueursQuiDevine: list[int]
    joueurQuiDevine: int
    tempsA: float
    tempsB: float

    MessageConsole(DEVINETTE_STR)
    # On affiche le titre du jeu
    # On affiche les règles du jeu
    regles()

    scores = [[0, 0], [1, 0]]
    listStatistiques = []

    if joueurs[0].robot and joueurs[1].robot:
        # On défini la liste de tout les nombres max possible (tous les multiples de 10 entre 10 et 50)
        listeNbMax = []
        compteur = 0

        while compteur < 5:
            listeNbMax.append((compteur + 1) * 10)
            compteur += 1
    else:
        listeNbMax = [None]

    for nbMaxListe in listeNbMax:

        # On crée une nouvelle statistique
        statistique = StatistiqueJeu()
        statistique.nomJeu = "Devinette"
        statistique.temps = [[], []]
        statistique.victoire = None
        statistique.valeurParticuliere = nbMaxListe
        statistique.difficultes = []

        if joueurs[0].robot and joueurs[0].difficulte:
            statistique.difficultes.append(joueurs[0].difficulte)
        else:
            statistique.difficultes.append("Humain")

        if joueurs[1].robot and joueurs[1].difficulte:
            statistique.difficultes.append(joueurs[1].difficulte)
        else:
            statistique.difficultes.append("Humain")


        # Si le nombre maximum n'est pas défini, on demande au premier joueur de le choisir
        if nbMaxListe is None:
            nombreMax = -1
            if not joueurs[0].robot:
                while nombreMax < 10 :
                    nombreMax = int(input(f"{joueurs[0].nom} : Choisissez un nombre maximum : \n"))
                    if nombreMax < 10 :
                        print("Le nombre maximum doit être supérieur à 10")
            else:
                nombreMax = randint(1, 100) * 10

            # Permet de définir le nombre de points du joueur 2 en fonction du nombre maximum
            scores[1][1] = nombreMax//10

            # On demande au premier joueur de choisir un nombre
            nombreCible = -1
            if not joueurs[0].robot:
                while nombreCible <= 0 or nombreCible > nombreMax :
                    nombreCible = int(input(f"{joueurs[0].nom}: Choisissez le nombre à faire deviner entre 1 et {nombreMax} : \n"))
                    if nombreCible <= 0 or nombreCible > nombreMax :
                        print(f"Le nombre choisi doit être compris entre 1 et {nombreMax}")
        else:
            nombreMax = nbMaxListe
            nombreCible = randint(1, nombreMax)

        # Ce programme s'exécute pour chaque manches, tant qu'il n'a pas gagner
        MessageConsole(f"{joueurs[0].nom} a choisi un nombre entre 1 et {nombreMax}, à toi de le deviner !")

        listeJoueursQuiDevine = [1]
        if joueurs[0].robot and joueurs[1].robot:
            listeJoueursQuiDevine.append(0)

        compteur = 0
        while compteur < len(listeJoueursQuiDevine):
            joueurQuiDevine = listeJoueursQuiDevine[compteur]

            jeuEnCours = True
            while jeuEnCours:
                
                tempsA = time()
                nombreSelect = DemanderNombre(joueurs[joueurQuiDevine], nombreMax)
                tempsB = time()
                statistique.temps[joueurQuiDevine].append(tempsB - tempsA)

                MessageConsole("")
                DemanderReponse(joueurs, nombreSelect, nombreCible, scores)
                
                if nombreSelect == nombreCible :
                    jeuEnCours = False

            compteur += 1

        listStatistiques.append(statistique)

    if len(listStatistiques) > 0 and joueurs[0].robot and joueurs[1].robot:
        print(f"Long statistiques: {len(listStatistiques)}")
        GenererFichierCSV(listStatistiques)

    return scores