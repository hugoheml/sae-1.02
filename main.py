from random import random
from devinette import Devinette
from allumettes import Allumettes
from morpion import Morpion
from puissance import Puissance4
from constants import MENU_STR
from score import GererScoresJeux, RecupererScores, EnregistrerScores, ScoreJeux, GererMenuScores, VerifierScore
from utils import MessageConsole

def ChoixUtilisateurs() -> list[str]:
    # Fonction qui demande à l'utilisateur de rentrer les identifiants des joueurs
    # Ne prends rien en argument
    # Si les identifiants existent les utilisateurs sont connectés
    # Si les identifiants n'existent pas les utilisateurs sont créés
    # Renvoie les identifiants des joueurs sous forme de liste
    utilisateur1: str
    utilisateur2: str


    utilisateur1 = ""
    utilisateur2 = ""
    MessageConsole("\n")
    while len(utilisateur1) < 3 or len(utilisateur1) > 10 :
        utilisateur1 = str(input("Entrez l'identifiant du joueur 1 (entre 3 et 10 caractères) : \n"))

        if len(utilisateur1) < 3 or len(utilisateur1) > 10 :
            print(" \nL'identifiant ne correspond pas aux critères demandés.")

    while len(utilisateur2) < 3 or len(utilisateur2) > 10 or utilisateur2 == utilisateur1 :
        utilisateur2 = str(input("\nEntrez l'identifiant du joueur 2 (entre 3 et 10 caractères & différent du joueur 1) : \n"))

        if utilisateur2 == utilisateur1 :
            print(" \nL'identifiant du joueur 2 est le même que celui du joueur 1.")

        elif len(utilisateur2) < 3 or len(utilisateur2) > 10 :
            print(" \nL'identifiant ne correspond pas aux critères demandés.")

    return [utilisateur1, utilisateur2]

def ChoisirOrdreJoueur(utilisateurs: list[str]) -> list[str] :
    # Prends en argument une liste de 2 utilisateurs sous forme de str
    # Renvoie une autre liste d'utilisateurs où l'utilisateur d'indice 0 est le premier joueur qui doit jouer

    if int(random()) == 0:
        return [utilisateurs[0], utilisateurs[1]]
    else:
        return [utilisateurs[1], utilisateurs[0]]

def AfficherMenu(utilisateur1 : str) -> None :
    # Prends en argument le nom du joueur sous forme de str qui doit choisir le jeu
    # Nettoie le terminal
    # Ne renvoie rien, mais affiche le menu dans le terminal

    MessageConsole(MENU_STR)
    print(f"\n{utilisateur1}: que voulez-vous faire ? :\n")
    print("1. Jouer à devinette")
    print("2. Jouer aux allumettes")
    print("3. Jouer au morpion") 
    print("4. Jouer au puissance 4")
    print("5. Afficher les scores\n")
    print("6. Quitter\n")

def DemanderRejouer(utilisateur1: str) -> bool :
    # Prends en argument le nom du joueur qui doit choisir s'il veut rejouer
    # Ne renvoie rien, mais affiche le menu dans le terminal

    rejouer: str

    rejouer = str(input(f"\n{utilisateur1}: voulez-vous rejouer [o] [n] ?"))
    return rejouer == "o"

def GererMenu(listeJoueurs: list[str], scores: ScoreJeux) -> None :
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
    Joueur1: str
    Joueur2: str

    arreterProgramme = False 
    choixMenu = -1

    while not arreterProgramme : 
        while choixMenu < 1 or choixMenu > 6 :
            choixMenu = int(input(""))
            if choixMenu < 1 or choixMenu > 6 :
                print("Le numéro du jeu n'est pas valide.")

        rejouer = True
        if choixMenu == 1:
            while rejouer :
                Joueur1, Joueur2 = ChoisirOrdreJoueur(listeJoueurs)
                
                listeScoreAAjouter = Devinette([Joueur1, Joueur2])
                GererScoresJeux(scores.devinette, listeScoreAAjouter, Joueur1, Joueur2)
                
                rejouer = DemanderRejouer(listeJoueurs[0])

        elif choixMenu == 2:
            while rejouer :
                Joueur1, Joueur2 = ChoisirOrdreJoueur(listeJoueurs)
                
                listeScoreAAjouter = Allumettes([Joueur1, Joueur2])
                GererScoresJeux(scores.allumettes, listeScoreAAjouter, Joueur1, Joueur2)
                
                rejouer = DemanderRejouer(listeJoueurs[0])

        elif choixMenu == 3:
            while rejouer :
                Joueur1, Joueur2 = ChoisirOrdreJoueur(listeJoueurs)
                

                listeScoreAAjouter = Morpion([Joueur1, Joueur2])
                GererScoresJeux(scores.morpion, listeScoreAAjouter, Joueur1, Joueur2)
                
                rejouer = DemanderRejouer(listeJoueurs[0])

        
        elif choixMenu == 4:
            while rejouer :
                Joueur1, Joueur2 = ChoisirOrdreJoueur(listeJoueurs)
                
                listeScoreAAjouter = Puissance4([Joueur1, Joueur2])
                GererScoresJeux(scores.puissance, listeScoreAAjouter, Joueur1, Joueur2)
                
                rejouer = DemanderRejouer(listeJoueurs[0])

        elif choixMenu == 5:
            GererMenuScores(scores)     

        elif choixMenu == 6:
            arreterProgramme = True

            # Sauvegarde en fichier binaires les scores
            EnregistrerScores(scores)
            print("Les scores ont été enregistrés")
        if choixMenu != 6:
            AfficherMenu(listeJoueurs[0])
            choixMenu = -1


if __name__ == "__main__" :
    listeJoueurs: list[str]

    listeJoueurs = ChoixUtilisateurs()
    scores = RecupererScores()

    for joueur in listeJoueurs:
        VerifierScore(scores.morpion, joueur)
        VerifierScore(scores.allumettes, joueur)
        VerifierScore(scores.devinette, joueur)
        VerifierScore(scores.puissance, joueur)

    AfficherMenu(listeJoueurs[0])
    GererMenu(listeJoueurs, scores)