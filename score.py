from typing import BinaryIO 
from constants import SCORE_FILE_NAME, SCORE_STR
import pickle
from utils import MessageConsole, Joueur

class JoueurScore:
    nom: str
    score: int

class ScoreJeux:
    morpion: list[JoueurScore]
    allumettes: list[JoueurScore]
    devinette: list[JoueurScore]
    puissance: list[JoueurScore]


def ChercherJoueur(scoreJeu: list[JoueurScore], joueur: str) -> int:
    # Prends la liste des joueurs du jeu et le nom du joueur en argument
    # Retourne l'indice du joueur dans la liste des joueurs du jeu

    index: int
    compteur: int

    index = -1
    compteur = 0

    while compteur < len(scoreJeu) and index == -1:
        if scoreJeu[compteur].nom == joueur:
            index = compteur
        compteur += 1
    return index

def TrierScores(tableau: list[JoueurScore]) -> None:
    # Prends en argument un tableau de joueurs
    # Ne retourne rien
    # Trie le tableau à l'aide du tri par insertion

    n: int
    compteur: int
    compteur2: int
    temp: JoueurScore

    n = len(tableau)

    for compteur in range(1, n):
        temp = tableau[compteur]
        compteur2 = compteur - 1
        while compteur2 >= 0 and tableau[compteur2].score < temp.score:
            tableau[compteur2 + 1] = tableau[compteur2]
            compteur2 = compteur2 - 1
        tableau[compteur2 + 1] = temp

def RecupererScores() -> ScoreJeux:
    # Ne prends rien en argument
    # Retourne un objet ScoreJeux à partir du fichier, trié par ordre croissant
    # Si le fichier n'existe pas, retourne un objet ScoreJeux vide

    fichier: BinaryIO
    score: ScoreJeux

    try:
        fichier = open(SCORE_FILE_NAME, "rb")
        
        score = pickle.load(fichier)
        TrierScores(score.morpion)
        TrierScores(score.allumettes)
        TrierScores(score.devinette)
        TrierScores(score.puissance)

        fichier.close()
    
    except FileNotFoundError:
        score = ScoreJeux()
        score.morpion = []
        score.allumettes = []
        score.devinette = []
        score.puissance = []

    return score

def EnregistrerScores(score: ScoreJeux) -> None:
    # Prends un objet ScoreJeux en argument
    # Ne retourne rien
    # Enregistre les données dans le fichier

    fichier: BinaryIO

    fichier = open(SCORE_FILE_NAME, "wb")
    pickle.dump(score, fichier)
    fichier.close()

def AjouterScore(scoreJeu: list[JoueurScore], joueur: Joueur, score: int) -> None:
    # Prends la liste des scores des joueurs du jeu, le nom du joueur et le score en argument
    # Ne retourne rien
    # Ajoute le score dans l'objet ScoreJeux
    # Si vous souhaitez enlever des points, mettez un score négatif

    joueurScore: JoueurScore
    index: int

    index = ChercherJoueur(scoreJeu, joueur.nom)
    if index == -1:
        joueurScore = JoueurScore()
        joueurScore.nom = joueur.nom
        joueurScore.score = score

        scoreJeu.append(joueurScore)
        index = len(scoreJeu) - 1
    else:
        joueurScore = scoreJeu[index]
    
        # On vérifie que le score ne soit pas négatif
        if (joueurScore.score + score) < 0:
            joueurScore.score = 0
        else:
            joueurScore.score += score

    if score < 0:
        print(f"{joueur.nom} a perdu {score*-1} points")
    elif score > 0:
        print(f"{joueur.nom} a gagné {score} points")

def VerifierScore(scoreJeu: list[JoueurScore], joueur: Joueur) -> None:
    # Prends la liste des scores des joueurs du jeu, le nom du joueur en argument
    # Vérifies que le joueur existe bien dans la liste des scores et le rajoute si ce n'est pas le cas

    index: int

    index = ChercherJoueur(scoreJeu, joueur.nom)
    if index == -1:
        # On ajoute 0 au score du joueur pour l'obliger à être mis dans la liste des scores
        AjouterScore(scoreJeu, joueur, 0)


# Fonction du menu
def AfficherMenu() -> None:
    """
        Ne prends rien en argument et ne renvoie rien, affiche simplement le menu d'affichage des scores
    """
    print("\nQue voulez-vous faire ?\n")
    print("1. Voir les scores du jeu morpion")
    print("2. Voir les scores du jeu allumettes")
    print("3. Voir les scores du jeu devinette")
    print("4. Voir les scores du jeu puissance 4")
    print("5. Voir le score total des joueurs")
    print("6. Quitter\n")

def AfficherScoresJoueurs(listeJoueurs: list[JoueurScore]) -> None:
    # Prends une liste de joueurs en argument
    # Affiche les scores des joueurs
    # Ne retourne rien

    compteur: int

    print("")
    for compteur in range(len(listeJoueurs)):
        print(f"{compteur + 1}. {listeJoueurs[compteur].nom} : {listeJoueurs[compteur].score}")

def AfficherScoreJeu(scores: ScoreJeux, nomJeu: str) -> None:
    # Prends un objet ScoreJeux et le nom du jeu en argument
    # Affiche les scores du jeu
    # Ne retourne rien

    scoresJoueurs: list[JoueurScore]
    scoresJoueurs = []

    if nomJeu == "morpion":
        scoresJoueurs = scores.morpion
    elif nomJeu == "allumettes":
        scoresJoueurs = scores.allumettes
    elif nomJeu == "devinette":
        scoresJoueurs = scores.devinette
    elif nomJeu == "puissance 4":
        scoresJoueurs = scores.puissance

    if len(scoresJoueurs) == 0:
        print(f"\nIl n'y a pas encore de scores du jeu : {nomJeu}")
    else:
        print("\nVoici les scores du jeu", nomJeu," :")
    AfficherScoresJoueurs(scoresJoueurs)

def AjouterScoreListe(scoresTotal: list[JoueurScore], scoresJeu: list[JoueurScore]) -> list[JoueurScore]:
    # Prends deux arugments, la liste des joueurs où on va ajouter les scores et la liste des joueurs du jeu

    joueur: JoueurScore
    nouveauJoueur: JoueurScore
    index: int

    for joueur in scoresJeu:
        index = ChercherJoueur(scoresTotal, joueur.nom)
        if index == -1:
            # On créer une nouvelle instance de joueur pour éviter les problèmes de références
            nouveauJoueur = JoueurScore()
            nouveauJoueur.nom = joueur.nom
            nouveauJoueur.score = joueur.score

            scoresTotal.append(nouveauJoueur)
        else:
            scoresTotal[index].score += joueur.score

    return scoresTotal

def AfficherScores(scores: ScoreJeux) -> None:
    # Prends en argument la liste des scores et affiche les scores de chaque joueurs, cumulés
    
    scoresTotal: list[JoueurScore]

    scoresTotal = []
    AjouterScoreListe(scoresTotal, scores.morpion)
    AjouterScoreListe(scoresTotal, scores.allumettes)
    AjouterScoreListe(scoresTotal, scores.devinette)
    AjouterScoreListe(scoresTotal, scores.puissance)

    TrierScores(scoresTotal)

    print("Voici les scores de tous les jeux")
    AfficherScoresJoueurs(scoresTotal)


def GererScoresJeux(scores: list[JoueurScore], listeScoreAAjouter: list[list[int]], listeJoueurs: list[Joueur]) -> None:
    # Prends en argument la liste des scores, la liste des scores à ajouter, le nom du joueur 1 et le nom du joueur 2
    # Ajoute les scores à la liste des scores
    # Ne retourne rien

    print()
    for scoreAAjouter in listeScoreAAjouter:
        if listeJoueurs[scoreAAjouter[0]].robot:
            continue

        if scoreAAjouter[1] == 0:
            if scoreAAjouter[0] == 0:
                print(f"{listeJoueurs[0]} n'a pas gagné de points")
            else:
                print(f"{listeJoueurs[1]} n'a pas gagné de points")
        else:
            if scoreAAjouter[0] == 0:
                AjouterScore(scores, listeJoueurs[0], scoreAAjouter[1])
            else:
                AjouterScore(scores, listeJoueurs[1], scoreAAjouter[1])
    

def GererMenuScores(scores: ScoreJeux) -> None:
    """
        Ne prends rien en argument et ne renvoie rien, gère simplement l'affichage des scores
    """

    choix: int

    choix = -1
    MessageConsole(SCORE_STR)

    while choix != 6:
        AfficherMenu()
        choix = int(input("Votre choix : "))

        if choix == 1:
            AfficherScoreJeu(scores, "morpion")
        elif choix == 2:
            AfficherScoreJeu(scores, "allumettes")
        elif choix == 3:
            AfficherScoreJeu(scores, "devinette")
        elif choix == 4:
            AfficherScoreJeu(scores, "puissance 4")
        elif choix == 5:
            AfficherScores(scores)
        elif choix == 6:
            print("Au revoir !")
        else:
            print("Choix invalide, veuillez réessayer")