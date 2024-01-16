from constants import MORPION_STR, REGLES_STR, JEU_STR
from utils import MessageConsole, Joueur
from random import randint
from statistiques import StatistiqueJeu, GenererFichierCSV
from time import time

def regles() -> None:
	# Ne prends aucun argument
	# Ne renvoie rien, mais affiche les règles du jeu dans le terminal

	print(REGLES_STR)
	print(" - Le jeu se joue à deux joueurs, chacun leur tour, ils doivent placer un pion sur une case vide")
	print(" - Le premier joueur qui aligne trois pions à gagné\n")
	print(JEU_STR)

def AfficherPlateau(board: list[list[int]]) -> None:
	# Prends en argument le plateau de jeu (une liste de listes d'entiers)
	# Ne renvoie rien, mais affiche le plateau de jeu dans le terminal

	ligne: int
	col: int
	_compteur: int

	# On affiche le plateau de jeu
	for ligne in range(len(board)):
		for col in range(len(board[ligne])):
			if board[ligne][col] == 0:
				print("  ", end="")
			elif board[ligne][col] == 1:
				print(" X", end="")
			elif board[ligne][col] == 2:
				print(" O", end="")

			if col != 2:
				print(" | ", end="")
			if col == 2 :
				print("   ",ligne + 1, end="")
				
		print()
		if ligne < 2:
			for _compteur in range(12):
				print("―", end="")
		print()
	print(" 1    2    3\n")

def DemanderCase(joueur: Joueur, board: list[list[int]]) -> list[int]:
	# Prends en argument le nom du joueur et le plateau de jeu
	# Renvoie une liste de deux entiers correspondant aux coordonnées de la case choisie par le joueur

	colonne: int
	ligne: int

	ligne = -1
	colonne = -1
	
	while ligne == -1 or colonne == -1 :
		# One demande au joueur de choisir une case

		if ligne < 1 or ligne > 3:
			ligne = int(input(f"{joueur.nom}: choisissez une ligne (1, 2, 3): "))
			if ligne < 1 or ligne > 3:
				print("Cette ligne n'existe pas, veuillez en choisir une autre")
				ligne = -1
		else:
			colonne = int(input(f"{joueur.nom}: choisissez une colonne (1, 2, 3): "))

			if colonne < 1 or colonne > 3:
				print("Cette colonne n'existe pas, veuillez en choisir une autre")
				colonne = -1
			else:
				# On vérifie que la case est vide
				if board[ligne - 1][colonne - 1] != 0:
					print("Cette case est déjà prise, veuillez en choisir une autre")
					colonne = -1
					ligne = -1

	MessageConsole("\n")
	return [colonne - 1, ligne -1]
	
def SelectionnerCase(joueur: Joueur, joueurId: int, board: list[list[int]], attendre: bool) -> None:
	# Prends en argument le nom du joueur, son identifiant (1 ou 2), le plateau de jeu et un booléen pour savoir si on doit attendre entre chaque coup
	# Modifie le plateau de jeu en fonction de la case choisie par le joueur

	coordonnes: list[int]
	cordonnesPossible: list[list[int]]
	casesVides: list[list[int]]
	victoire: int
	compteur: int
	compteur2: int
	adversaire: int
	pionPlace: bool

	if not joueur.robot:
		# On demande au joueur de choisir une case
		coordonnes = DemanderCase(joueur, board)

		# On modifie le plateau de jeu
		board[coordonnes[1]][coordonnes[0]] = joueurId
		print(f"{joueur.nom} a choisi la case {coordonnes[0] + 1}, {coordonnes[1] + 1}")
	else:

		if attendre:
			input("Appuyez sur entrée pour continuer")

		if joueur.difficulte == "facile":
			# On récupère une liste contenant toutes les cases vides
			casesVides = []
			for compteur in range(3):
				for compteur2 in range(3):
					if board[compteur][compteur2] == 0:
						casesVides.append([compteur2, compteur])
			
			# On choisit une case au hasard parmis la liste de case vide
			coordonnes = casesVides[randint(0, len(casesVides) - 1)]
			
			board[coordonnes[1]][coordonnes[0]] = joueurId
			print(f"{joueur.nom} a choisi la case {coordonnes[0] + 1}, {coordonnes[1] + 1}")

		elif joueur.difficulte == "difficile":
			# Si le joueur actuel peut gagner, il pose son pion et gagne.
			pionPlace = False

			for compteur in range(3):
				for compteur2 in range(3):
					if not pionPlace and board[compteur][compteur2] == 0:
						board[compteur][compteur2] = joueurId

						victoire = VerifierVictoire(board)

						if victoire == 0 or victoire == joueurId:
							pionPlace = True
							print(f"{joueur.nom} a choisi la case {compteur2 + 1}, {compteur + 1}")
						else:
							board[compteur][compteur2] = 0
			
			if not pionPlace:
				# Si le joueur n'a pas gagné, alors on vérifie si l'adversaire peut gagner
				adversaire = 1
				if joueurId == 1:
					adversaire = 2

				for compteur in range(3):
					for compteur2 in range(3):
						if board[compteur][compteur2] == 0:
							board[compteur][compteur2] = adversaire

							victoire = VerifierVictoire(board)

							if victoire == adversaire:
								pionPlace = True
								board[compteur][compteur2] = joueurId
								print(f"{joueur.nom} a choisi la case {compteur2 + 1}, {compteur + 1}")
							else:
								board[compteur][compteur2] = 0
			
			if not pionPlace:
				# Si la case du milieu est vide, on la choisit
				if board[1][1] == 0:
					board[1][1] = joueurId
					pionPlace = True
					print(f"{joueur.nom} a choisi la case 2, 2")
			
			if not pionPlace:
				cordonnesPossible = []
				# On tente de placer notre pion sur une case vide dans les coins
				if board[0][0] == 0:
					cordonnesPossible.append([0, 0])
				if board[0][2] == 0:
					cordonnesPossible.append([2, 0])
				if board[2][0] == 0:
					cordonnesPossible.append([0, 2])
				if board[2][2] == 0:
					cordonnesPossible.append([2, 2])

				if len(cordonnesPossible) > 0:
					coordonnes = cordonnesPossible[randint(0, len(cordonnesPossible) - 1)]
					board[coordonnes[1]][coordonnes[0]] = joueurId
					pionPlace = True
					print(f"{joueur.nom} a choisi la case {coordonnes[0] + 1}, {coordonnes[1] + 1}")

			if not pionPlace:
				# On tente de placer notre pion sur une case vide sur les bords
				cordonnesPossible = []
				if board[0][1] == 0:
					cordonnesPossible.append([1, 0])
				if board[1][0] == 0:
					cordonnesPossible.append([0, 1])
				if board[1][2] == 0:
					cordonnesPossible.append([2, 1])
				if board[2][1] == 0:
					cordonnesPossible.append([1, 2])

				if len(cordonnesPossible) > 0:
					coordonnes = cordonnesPossible[randint(0, len(cordonnesPossible) - 1)]
					board[coordonnes[1]][coordonnes[0]] = joueurId
					pionPlace = True
					print(f"{joueur.nom} a choisi la case {coordonnes[0] + 1}, {coordonnes[1] + 1}")

def VerifierVictoire(board: list[list[int]]) -> int:
	# Prends en argument le plateau de jeu
	# Renvoie un entier:
	# -1: si personne n'a gagné
	#  0: si le plateau est plein (match nul)
	#  1: si le joueur 1 a gagné
	#  2: si le joueur 2 a gagné

	resultat: int
	compteurA: int
	compteurB: int
	estPlein: bool

	# De base, personne n'a gagné
	resultat = -1

	# On vérifie d'abord les lignes
	compteurA = 0
	while resultat == -1 and compteurA < 3:
		if board[compteurA][0] != 0 and board[compteurA][0] == board[compteurA][1] and board[compteurA][1] == board[compteurA][2]:
			resultat = board[compteurA][0]
		
		compteurA += 1

	# On vérifie ensuite les colonnes
	compteurA = 0
	while resultat == -1 and compteurA < 3:
		if board[0][compteurA] != 0 and board[0][compteurA] == board[1][compteurA] and board[1][compteurA] == board[2][compteurA]:
			resultat = board[0][compteurA]
		
		compteurA += 1

	# On vérifie enfin les diagonales
	if resultat == -1 and board[1][1] != 0:
		if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
			resultat = board[1][1]
		elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
			resultat = board[1][1]

	# On vérifie si le plateau est plein
	if resultat == -1:
		# On considère que le plateau est plein
		estPlein = True
		compteurA = 0
		
		# On vérifie pour chaque ligne et chaque colonne si une case est vide
		# Si c'est le cas, le plateau n'est pas plein
		while estPlein and compteurA < 3:
			compteurB = 0

			while estPlein and compteurB < 3:
				if board[compteurA][compteurB] == 0:
					estPlein = False
				
				compteurB += 1
			
			compteurA += 1

		# Si le plateau est plein, on renvoie 0
		if estPlein:
			resultat = 0

	return resultat

def Morpion(joueurs: list[Joueur]):
    # Prends en argument une liste de deux chaînes de caractères correspondant aux noms des joueurs
    # Le premier joueur étant celui qui commence
    # Ne renvoies rien, mais fait fonctionner le jeu dans le terminal

	plateau: list[list[int]]
	joueurQuiJoue: int
	joueurQuiCommence: int
	resultat: int
	scores: list[list[int]]
	nbManches: list[int]
	listeStatistiques: list[StatistiqueJeu]
	statistique: StatistiqueJeu
	compteurA: int
	tempsA: float
	tempsB: float
	faireStatistiques: str

	# Trois valeurs d'entier sont possibles:
	# 0: case vide
	# 1: case prise par le joueur 1
	# 2: case prise par le joueur

	MessageConsole(MORPION_STR)
    # On affiche le titre du jeu
    # On affiche les règles du jeu
	regles()

	scores = [[0, 0], [1, 0]]
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

		# On initialise le plateau de jeu
		plateau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

		# On initialise les statistiques
		statistique = StatistiqueJeu()
		statistique.nomJeu = "Morpion"
		statistique.temps = [[], []]
		statistique.difficultes = []
		statistique.victoire = None
		statistique.valeurParticuliere = None
		if joueurs[0].difficulte and joueurs[1].difficulte:
			statistique.difficultes.append(joueurs[0].difficulte)
			statistique.difficultes.append(joueurs[1].difficulte)


		resultat = -1
		joueurQuiJoue = joueurQuiCommence

		# On affiche le plateau de jeu
		AfficherPlateau(plateau)

		# On lance le jeu
		while resultat == -1:

			# On demande au joueur de choisir une case
			tempsA = time()
			SelectionnerCase(joueurs[joueurQuiJoue], joueurQuiJoue + 1, plateau, faireStatistiques != "o")
			tempsB = time()

			# On enregistre le temps du joueur
			statistique.temps[joueurQuiJoue].append(tempsB - tempsA)

			# On affiche le plateau de jeu
			AfficherPlateau(plateau)
			
			# On vérifie si le joueur a gagné
			resultat = VerifierVictoire(plateau)

			# On change de joueur
			if joueurQuiJoue == 0:
				joueurQuiJoue = 1
			else:
				joueurQuiJoue = 0

		if resultat == 0:
			print("Match nul")

			scores[0][1] = 1
			scores[1][1] = 1

		else:
			print(f"Victoire du joueur {joueurs[resultat - 1].nom}")
			scores[resultat - 1][1] = 2

			if (resultat - 1) == 0:
				scores[1][1] = 0
			else:
				scores[0][1] = 0

		statistique.victoire = resultat - 1
		listeStatistiques.append(statistique)

	if len(nbManches) > 1:
		GenererFichierCSV(listeStatistiques)

	return scores