from random import random
from devinette import Devinette
from allumettes import Allumettes
from morpion import Morpion
from puissance import Puissance4
from constants import MENU_STR
from score import GererScoresJeux, RecupererScores, EnregistrerScores, ScoreJeux, GererMenuScores, VerifierScore
from utils import MessageConsole, Joueur

def ajout_utilisateur(listeUtilisateurs: list[Joueur]) -> None:
    # Prends en argument une liste de joueur
    # Ajoute un joueur à cette liste (passage par référence)

    utilisateur: Joueur
    utilisateur = Joueur()
    utilisateur.nom = ""
    utilisateur.robot = False
    utilisateur.difficulte = None
    robot: str
    difficulte: str
    numeroJoueur: int

    difficulte = ""
    robot = ""

    numeroJoueur = len(listeUtilisateurs) + 1

    while robot != "o" and robot != "n":
        robot = str(input(f"Voulez-vous que le joueur n°{numeroJoueur} soit un robot [o] [n] ? \n"))
        
        utilisateur.robot = robot == "o"

    if utilisateur.robot:
        while difficulte != "facile" and difficulte != "difficile":
            difficulte = str(input("Quelle difficulté voulez-vous [facile] [difficile] ? \n"))
            if difficulte != "facile" and difficulte != "difficile":
                print("La difficulté n'est pas valide")
            else :
                utilisateur.difficulte = difficulte
        
        utilisateur.nom = f"Bot{numeroJoueur} - {utilisateur.difficulte}"
    else:
        utilisateur.difficulte = None

        while len(utilisateur.nom) < 3 or len(utilisateur.nom) > 10 :
            utilisateur.nom = str(input(f"Entrez l'identifiant du joueur {numeroJoueur} (entre 3 et 10 caractères) : \n"))
            for joueur in listeUtilisateurs:
                if utilisateur.nom == joueur.nom:
                    utilisateur.nom = ""
            if len(utilisateur.nom) < 3 or len(utilisateur.nom) > 10:
                print(" \nL'identifiant ne correspond pas aux critères demandés.")


    listeUtilisateurs.append(utilisateur)


def ChoixUtilisateurs() -> list[Joueur]:
    # Fonction qui demande à l'utilisateur de rentrer les identifiants des joueurs
    # Ne prends rien en argument
    # Si les identifiants existent les utilisateurs sont connectés
    # Si les identifiants n'existent pas les utilisateurs sont créés
    # Renvoie les identifiants des joueurs sous forme de liste

    listeUtilisateurs: list[Joueur]
    listeUtilisateurs = []

    MessageConsole("")
    ajout_utilisateur(listeUtilisateurs)

    MessageConsole("")
    ajout_utilisateur(listeUtilisateurs)
    
    return listeUtilisateurs

def ChoisirOrdreJoueur(utilisateurs: list[Joueur]) -> list[Joueur] :
    # Prends en argument une liste de 2 utilisateurs sous forme de str
    # Renvoie une autre liste d'utilisateurs où l'utilisateur d'indice 0 est le premier joueur qui doit jouer

    if int(random()) == 0:
        return [utilisateurs[0], utilisateurs[1]]
    else:
        return [utilisateurs[1], utilisateurs[0]]

def AfficherMenu(utilisateur : str) -> None :
    # Prends en argument le nom du joueur sous forme de str qui doit choisir le jeu
    # Nettoie le terminal
    # Ne renvoie rien, mais affiche le menu dans le terminal

    MessageConsole(MENU_STR)
    print(f"\n{utilisateur}: que voulez-vous faire ? :\n")
    print("1. Jouer à devinette")
    print("2. Jouer aux allumettes")
    print("3. Jouer au morpion") 
    print("4. Jouer au puissance 4")
    print("5. Afficher les scores\n")
    print("6. Quitter\n")

def DemanderRejouer(administrateur: str) -> bool :
    # Prends en argument le nom de l'administrateur sous forme de str
    # Demande au joueur s'il veut rejouer
    # Renvoie True si le joueur veut rejouer, False sinon

    rejouer: str

    rejouer = str(input(f"\n{administrateur}: voulez-vous rejouer [o] [n] ?"))
    return rejouer == "o"

def GererMenu(listeJoueurs: list[Joueur], scores: ScoreJeux) -> None :
    # Prends en argument la liste des joueurs et la liste des scores
    # Ne renvoie rien
    # Récupère les scores des joueurs
    # Enregistre les scores des joueurs
    # Affiche le menu
    # Demande au joueur de choisir un jeu
    # Lance le jeu choisi
    # Demande au joueur s'il veut rejouer
    # Si oui, relance le jeu
    # Si non, affiche le menu

    rejouer: bool
    arreterProgramme: bool
    listeScoreAAjouter: list[list[int]]
    choixMenu: int
    joueurs: list[Joueur]

    # L'administrateur est le nom de la personne qui doit s'occuper de gérer les jeux qui sont joués
    administrateur: str

    arreterProgramme = False 
    choixMenu = -1

    # Par défaut, l'administrateur est le premier joueur de la liste
    administrateur = listeJoueurs[0].nom

    # Si le premier joueur est un robot, l'administrateur est le deuxième joueur
    if listeJoueurs[0].robot:
        administrateur = listeJoueurs[1].nom

    # Si les deux joueurs sont des robots, l'administrateur est demandé
    if listeJoueurs[0].robot and listeJoueurs[1].robot:
        administrateur = ""
        while administrateur != listeJoueurs[0].nom and administrateur != listeJoueurs[1].nom and len(administrateur) < 3 or len(administrateur) > 10:
            administrateur = str(input("Qui est l'administrateur ? \n"))
            if administrateur != listeJoueurs[0].nom and administrateur != listeJoueurs[1].nom and len(administrateur) < 3 or len(administrateur) > 10:
                print("L'administrateur ne doit pas être un des deux robots et doit contenir entre 3 et 10 caractères.")

    AfficherMenu(administrateur)
    while not arreterProgramme : 
        while choixMenu < 1 or choixMenu > 6 :
            choixMenu = int(input(""))
            if choixMenu < 1 or choixMenu > 6 :
                print("Le numéro du jeu n'est pas valide.")

        # On vide les infosParticulieres des deux joueurs
        listeJoueurs[0].infoParticulieres = None
        listeJoueurs[1].infoParticulieres = None

        rejouer = True
        if choixMenu == 1:
            while rejouer :
                joueurs = ChoisirOrdreJoueur(listeJoueurs)
                
                listeScoreAAjouter = Devinette(joueurs)
                GererScoresJeux(scores.devinette, listeScoreAAjouter, joueurs)
                
                if joueurs[0].robot and joueurs[1].robot:
                    rejouer = False
                    input("Appuyez sur entrer pour continuer")
                else:
                    rejouer = DemanderRejouer(administrateur)

        elif choixMenu == 2:
            while rejouer :
                joueurs = ChoisirOrdreJoueur(listeJoueurs)
                
                listeScoreAAjouter = Allumettes(joueurs)
                GererScoresJeux(scores.allumettes, listeScoreAAjouter, joueurs)
                
                if joueurs[0].robot and joueurs[1].robot:
                    rejouer = False
                    input("Appuyez sur entrer pour continuer")
                else:
                    rejouer = DemanderRejouer(administrateur)

        elif choixMenu == 3:
            while rejouer :
                joueurs = ChoisirOrdreJoueur(listeJoueurs)
                

                listeScoreAAjouter = Morpion(joueurs)
                GererScoresJeux(scores.morpion, listeScoreAAjouter, joueurs)
                
                if joueurs[0].robot and joueurs[1].robot:
                    rejouer = False
                    input("Appuyez sur entrer pour continuer")
                else:
                    rejouer = DemanderRejouer(administrateur)

        elif choixMenu == 4:
            if listeJoueurs[0].robot and listeJoueurs[1].robot:
                rejouer = False
                print("Malheureusement, nous ne supportons pas le Puissance 4 avec deux robots")
                input("Appuyez sur entrer pour continuer")
            while rejouer :
                joueurs = ChoisirOrdreJoueur(listeJoueurs)
                
                listeScoreAAjouter = Puissance4(joueurs)
                GererScoresJeux(scores.puissance, listeScoreAAjouter, joueurs)
                
                if joueurs[0].robot and joueurs[1].robot:
                    rejouer = False
                    input("Appuyez sur entrer pour continuer")
                else:
                    rejouer = DemanderRejouer(administrateur)

        elif choixMenu == 5:
            GererMenuScores(scores)     

        elif choixMenu == 6:
            arreterProgramme = True

            # Sauvegarde en fichier binaires les scores
            EnregistrerScores(scores)
            print("Les scores ont été enregistrés")
        if choixMenu != 6:
            AfficherMenu(administrateur)
            choixMenu = -1


if __name__ == "__main__" :
    listeJoueurs: list[Joueur]

    listeJoueurs = ChoixUtilisateurs()
    scores = RecupererScores()

    for joueur in listeJoueurs:
        VerifierScore(scores.morpion, joueur)
        VerifierScore(scores.allumettes, joueur)
        VerifierScore(scores.devinette, joueur)
        VerifierScore(scores.puissance, joueur)

    GererMenu(listeJoueurs, scores)