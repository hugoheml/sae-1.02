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

def DemanderNombre(joueur: Joueur, nombreMax: int, nombreCible: int) -> int :
    # Prends en argument le joueur qui doit deviner le nombre, le nombre maximum et le nombre à deviner
    # Et l'intervalle maximal dans lequel le nombre peut être choisi

    nombreSelect : int
    nombreMinJoueur : int
    nombreMaxJoueur : int
    ancienNbSelect : Optional[int]


    # On demande au joueur de choisir un nombre
    nombreSelect = -1

    if not joueur.robot:
        while nombreSelect <= 0 or nombreSelect > nombreMax :
            nombreSelect = int(input(f"\n{joueur.nom}: Proposez un nombre entre 1 et {nombreMax} : \n"))

            if nombreSelect <= 0 or nombreSelect > nombreMax :
                print(f"Le nombre choisi doit être compris entre 1 et {nombreMax}")

    elif joueur.difficulte == "facile":
        nombreSelect = randint(1, nombreMax)

    elif joueur.difficulte == "difficile":
        # On prends le nombre maximum et on le divise par deux
        # Si le nombre est plus grand que le nombre à deviner, on prends la moitié supérieur
        # Sinon on prends la moitié inférieur
        # On répète l'opération jusqu'à trouver le nombre à deviner
        # Si le nombre max / 2 est un float on prends le nombre entier supérieur

        if joueur.infoParticulieres is None:
            joueur.infoParticulieres = [1, nombreMax, -1]
        
        nombreMinJoueur = joueur.infoParticulieres[0]
        nombreMaxJoueur = joueur.infoParticulieres[1]
        ancienNbSelect = joueur.infoParticulieres[2]

        if ancienNbSelect != -1:
            # Algo en fonction de l'ancien nombre choisi
            if ancienNbSelect > nombreCible:
                if ancienNbSelect == nombreMax:
                    nombreMinJoueur = ancienNbSelect - 1
                else:
                    nombreMaxJoueur = ancienNbSelect

                joueur.infoParticulieres[1] = nombreMaxJoueur

            elif ancienNbSelect < nombreCible:
                nombreMinJoueur = ancienNbSelect
                joueur.infoParticulieres[0] = nombreMinJoueur

        nombreSelect = nombreMinJoueur + (nombreMaxJoueur - nombreMinJoueur + 1) // 2     
        joueur.infoParticulieres[2] = nombreSelect

    return nombreSelect

def DemanderReponse(joueurs: list[Joueur], nombreSelect: int, nombreCible: int, scores: list[list[int]], joueurQuiDevine: int, joueurQuiDonneReponses: int) -> None :
    # Prends en argument une liste de deux chaines de caractères représentant les noms des joueurs
    # Le nombre choisi par le joueur ainsi que celui qui doit le deviner
    # Et une liste de liste de deux entiers représentant l'indice du joueur et le score à ajouter
    # Et le joueur qui devine et celui qui doit donner les réponses
    # Ne renvoies rien, mais envoie dans le terminal la réponse du joueur

    reponseSelect: int
    demandeEnCours : bool
    
    # On demande au joueur de choisir une réponse
    demandeEnCours = True

    MessageConsole("\n")
    print(f"\n{joueurs[joueurQuiDevine].nom} propose le nombre : {nombreSelect}")
    print(f"Le nombre à deviner est : {nombreCible}")
    print(f"\n{joueurs[joueurQuiDonneReponses].nom}: Sélectionnez une réponse parmis :")
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
                    scores[joueurQuiDonneReponses][1] = scores[joueurQuiDonneReponses][1]-1

                else :
                    MessageConsole(f"{joueurs[0].nom}: Le nombre est plus grand")
                    scores[joueurQuiDonneReponses][1] = scores[joueurQuiDonneReponses][1]+1
                    demandeEnCours = False

            elif reponseSelect == 2 :
                if nombreSelect <= nombreCible :
                    print("Bien tenté mais non, faut pas tricher, réessayez")
                    scores[joueurQuiDonneReponses][1] = scores[joueurQuiDonneReponses][1]-1

                else :
                    MessageConsole(f"{joueurs[0].nom}: Le nombre est plus petit")
                    scores[joueurQuiDonneReponses][1] = scores[joueurQuiDonneReponses][1]+1
                    demandeEnCours = False

            elif reponseSelect == 3 :
                if nombreSelect == nombreCible :
                    MessageConsole(f"{joueurs[0].nom}: Bravo {joueurs[1].nom} tu as gagné")
                    scores[joueurQuiDonneReponses][1] = scores[joueurQuiDonneReponses][1]+1
                    demandeEnCours = False

                else :
                    print("Bien tenté mais non, faut pas tricher, réessayez")
                    scores[joueurQuiDonneReponses][1] = scores[joueurQuiDonneReponses][1]-1

        scores[joueurQuiDevine][1] = scores[joueurQuiDevine][1]-1
    else:
        if nombreSelect > nombreCible:
            MessageConsole(f"{joueurs[0].nom}: Le nombre est plus petit")

        elif nombreSelect < nombreCible:
            MessageConsole(f"{joueurs[0].nom}: Le nombre est plus grand")

        elif nombreSelect == nombreCible:
            MessageConsole(f"{joueurs[0].nom}: Bravo {joueurs[1].nom} tu as gagné")

        scores[joueurQuiDevine][1] = scores[joueurQuiDevine][1]-1
                

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
    joueurQuiDonneReponses: int
    tempsA: float
    tempsB: float
    faireStatistiques: str

    MessageConsole(DEVINETTE_STR)
    # On affiche le titre du jeu
    # On affiche les règles du jeu
    regles()

    scores = [[0, 0], [1, 0]]
    listStatistiques = []

    faireStatistiques = ""
    if joueurs[0].robot and joueurs[1].robot:
        # On défini la liste de tout les nombres max possible (tous les multiples de 10 entre 10 et 50)
        listeNbMax = []

        while faireStatistiques != "o" and faireStatistiques != "n":
            faireStatistiques = input("Voulez-vous effectuer des statistiques ? [o/n] ")

        if faireStatistiques == "o":
            compteur = 0
            while compteur < 10:
                listeNbMax.append((compteur + 1) * 10)
                compteur += 1
        else:
            listeNbMax = [None]

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

        if joueurs[0].difficulte and joueurs[1].difficulte:
            statistique.difficultes.append(joueurs[0].difficulte)
            statistique.difficultes.append(joueurs[1].difficulte)


        # Si le nombre maximum n'est pas défini, on demande au premier joueur de le choisir
        if nbMaxListe is None:
            nombreMax = -1
            if not joueurs[0].robot:
                while nombreMax < 10 :
                    nombreMax = int(input(f"{joueurs[0].nom} : Choisissez un nombre maximum : \n"))
                    if nombreMax < 10 :
                        print("Le nombre maximum doit être supérieur à 10")
            else:
                nombreMax = randint(11, 100)

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
                nombreCible = randint(1, nombreMax)
        else:
            nombreMax = nbMaxListe
            nombreCible = randint(1, nombreMax)

        listeJoueursQuiDevine = [1]
        if joueurs[0].robot and joueurs[1].robot:
            listeJoueursQuiDevine.append(0)

        compteur = 0
        while compteur < len(listeJoueursQuiDevine):
            joueurQuiDevine = listeJoueursQuiDevine[compteur]
            if joueurQuiDevine == 0:
                joueurQuiDonneReponses = 1
            else:
                joueurQuiDonneReponses = 0

            joueurs[joueurQuiDevine].infoParticulieres = None
            nombreSelect = -1

            
            MessageConsole(f"{joueurs[joueurQuiDonneReponses].nom} a choisi un nombre entre 1 et {nombreMax}, à toi de le deviner !")

            jeuEnCours = True
            while jeuEnCours:
                
                tempsA = time()
                nombreSelect = DemanderNombre(joueurs[joueurQuiDevine], nombreMax, nombreCible)
                tempsB = time()
                statistique.temps[joueurQuiDevine].append(tempsB - tempsA)

                if joueurs[joueurQuiDevine].robot:
                    print(f"{joueurs[joueurQuiDevine].nom} a choisi le nombre {nombreSelect}")
                
                if faireStatistiques != "o" and (joueurs[0].robot and joueurs[1].robot):
                    input(f"Appuyez sur entrée pour continuer")

                MessageConsole("")
                DemanderReponse(joueurs, nombreSelect, nombreCible, scores, joueurQuiDevine, joueurQuiDonneReponses)

                if faireStatistiques != "o" and (joueurs[0].robot and joueurs[1].robot):
                    input(f"Appuyez sur entrée pour continuer")
                
                if nombreSelect == nombreCible :
                    jeuEnCours = False

            compteur += 1

        if faireStatistiques == "o":
            listStatistiques.append(statistique)

    if faireStatistiques == "o":
        GenererFichierCSV(listStatistiques)

    return scores