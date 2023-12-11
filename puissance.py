from constants import PUISSANCE_STR, REGLES_STR, JEU_STR
from utils import MessageConsole

def regles() -> None:
	# Ne prends aucun argument
	# Ne renvoie rien, mais affiche les règles du jeu dans le terminal

	print(REGLES_STR)
	print(" - Le jeu se joue à deux joueurs, chacun leur tour, ils doivent placer un pion sur une case vide")
	print(" - Le premier joueur qui aligne quatre pions à gagné\n")
	print(JEU_STR)


def AfficherPlateau(board: list[list[int]], afficherRegles: bool) -> None:
	# Prends en argument le plateau de jeu et un booléen qui indique si les règles doivent être affichées
	# Ne renvoie rien, mais affiche le plateau de jeu dans le terminal
	
	ligne: int
	colonne: int
	compteur: int

	# On affiche le plateau de jeu
	MessageConsole(PUISSANCE_STR)
	if afficherRegles:
		regles()
	
	for ligne in range(len(board[0])):
		print(" | ", end="")
		for colonne in range(len(board)):
			if board[colonne][ligne] == -1:
				print("◯", end=" ")
			elif board[colonne][ligne] == 0:
				print("🔴", end="")
			else:  
				print("🔵", end="")

			print(" | ", end="")
		print()

	for compteur in range(0, len(board)):
		if compteur == 0:
			print("    ", end="")
		print(compteur + 1, end="    ")

def SelectionnerCase(joueur: str, joueurId: int, pions: list[str], board: list[list[int]]) -> None:
	# Prends en argument le nom du joueur et le plateau de jeu
	# Ne retourne rien et modifie le jeu
	# Si la case est déjà prise, la fonction redemande une case au joueur

	colonne: int 
	compteur :int
	ligne = -1

	colonne = -1
	while (colonne < 1 or colonne > 7) or ligne == -1:
		# On demande au joueur de choisir une case
		colonne = int(input(f"{pions[joueurId]} {joueur}: choisissez une colonne (1, 2, 3, 4, 5, 6, 7): "))

		if colonne < 1 or colonne > 7:
			print("Cette case n'existe pas, veuillez en choisir une autre")
		else:
			ligne = -1
			for compteur in range(len(board[colonne - 1])):
				if board[colonne - 1][compteur] == -1:
					ligne = compteur

			if ligne == -1:
				print("Cette colonne est pleine, veuillez en choisir une autre")
			else:
				board[colonne - 1][ligne] = joueurId


def Verifier_victoire_ligne(board: list[list[int]]) -> int:
	# Prends en argument le plateau de jeu
	# Retourne l'identifiant du joueur qui a gagné
	# Si aucun joueur n'a gagné, retourne -1
	# Si le joueur  1 a gagné renvoie 1
	# Si le joueur 2 a gagné renvoie 2

	ligne: int
	colonne: int
	resultat: int

	resultat = -1
	for ligne in range(len(board[0])):
		for colonne in range(len(board) - 3):
			if board[colonne][ligne] != -1 and board[colonne][ligne] == board[colonne + 1][ligne] and board[colonne][ligne] == board[colonne + 2][ligne] and board[colonne][ligne] == board[colonne + 3][ligne]:
				resultat = board[colonne][ligne] + 1
				
	return resultat
	
def Verifier_victoire_colonne(board: list[list[int]]) -> int:
	# Prends en argument le plateau de jeu
	# Retourne l'identifiant du joueur qui a gagné
	# Si aucun joueur n'a gagné, retourne -1
	# Si le joueur  1 a gagné renvoie 1
	# Si le joueur 2 a gagné renvoie 2

	ligne: int
	colonne: int
	resultat: int

	resultat = -1
	for colonne in range(len(board)):
		for ligne in range(len(board[0]) - 3):
			if board[colonne][ligne] != -1 and board[colonne][ligne] == board[colonne][ligne + 1] and board[colonne][ligne] == board[colonne][ligne + 2] and board[colonne][ligne] == board[colonne][ligne + 3]:
				resultat = board[colonne][ligne] + 1

	return resultat

def Verifier_victoire_diagonale(board: list[list[int]]) -> int:
	# Prends en argument le plateau de jeu
	# Retourne l'identifiant du joueur qui a gagné
	# Si aucun joueur n'a gagné, retourne -1
	# Si le joueur  1 a gagné renvoie 1
	# Si le joueur 2 a gagné renvoie 2

	ligne: int
	colonne: int
	resultat: int

	resultat = -1
	for colonne in range(len(board) - 3):
		# On vérifie d'après le pion, jusqu'en bas à droite
		if resultat == -1:
			for ligne in range(len(board[0]) - 3):
				if board[colonne][ligne] != -1 and board[colonne][ligne] == board[colonne + 1][ligne + 1] and board[colonne][ligne] == board[colonne + 2][ligne + 2] and board[colonne][ligne] == board[colonne + 3][ligne + 3]:
					resultat = board[colonne][ligne] + 1
		if resultat == -1:
			# On vérifie d'après le pion, jusqu'en bas à gauche
			for ligne in range(3, len(board[0])):
				if board[colonne][ligne] != -1 and board[colonne][ligne] == board[colonne + 1][ligne - 1] and board[colonne][ligne] == board[colonne + 2][ligne - 2] and board[colonne][ligne] == board[colonne + 3][ligne - 3]:
					resultat = board[colonne][ligne] + 1

	return resultat

def VerifierVictoire(board: list[list[int]]) -> int:
	# Prends en argument le plateau de jeu
	# Retourne l'identifiant du joueur qui a gagné
	# Si aucun joueur n'a gagné, retourne -1
	# Si le tableau est plein et que personne n'a gagné, retourne 0
	# Si le joueur  1 a gagné renvoie 1
	# Si le joueur 2 a gagné renvoie 2

	resultat: int
	caseVide: bool
	ligne: int
	colonne: int

	resultat = Verifier_victoire_ligne(board)
	if resultat == -1:
		resultat = Verifier_victoire_colonne(board)
	if resultat == -1:
		resultat = Verifier_victoire_diagonale(board)

	if resultat == -1:
		caseVide = False
		for ligne in range(len(board[0])):
			for colonne in range(len(board)):
				if board[colonne][ligne] == -1:
					caseVide = True

		if caseVide == False:
			resultat = 0

	return resultat

def Puissance4(joueurs: list[str]):
    # Prends en argument une liste de deux chaînes de caractères correspondant aux noms des joueurs
    # Le premier joueur étant celui qui commence
    # Ne renvoies rien, mais fait fonctionner le jeu dans le terminal

	plateau: list[list[int]]
	pions: list[str]
	joueurQuiJoue: int
	resultat: int
	scores: list[list[int]]
	# Trois valeurs d'entier sont possibles:
	# 0: case vide
	# 1: case prise par le joueur 1
	# 2: case prise par le joueur

	# Nettoi le terminal
    # On affiche le titre du jeu
    # On affiche les règles du jeu

	MessageConsole(PUISSANCE_STR)
	regles()

	# On initialise le plateau de jeu
	plateau = [
		[-1, -1, -1, -1, -1, -1],
		[-1, -1, -1, -1, -1, -1],
		[-1, -1, -1, -1, -1, -1],
		[-1, -1, -1, -1, -1, -1],
		[-1, -1, -1, -1, -1, -1],
		[-1, -1, -1, -1, -1, -1],
		[-1, -1, -1, -1, -1, -1],
	]
	scores = [[0, 0], [1, 0]]

	pions = ["🔴", "🔵"]

	resultat = -1
	joueurQuiJoue = 0

    # On lance le jeu
	AfficherPlateau(plateau, True)
	while resultat == -1:
		# On demande au joueur de choisir une case
		print()
		SelectionnerCase(joueurs[joueurQuiJoue], joueurQuiJoue, pions, plateau)

		# On affiche le plateau de jeu
		AfficherPlateau(plateau, False)

		# On change de joueur
		if joueurQuiJoue == 0:
			joueurQuiJoue = 1
		else:
			joueurQuiJoue = 0

		# On vérifie si le joueur a gagné
		resultat = VerifierVictoire(plateau)

	if resultat == 0:
		print("\nMatch nul")

		scores[0][1] = 2 
		scores[1][1] = 2
	else:
		print(f"\nVictoire du joueur {joueurs[resultat - 1]} avec les pions {pions[resultat - 1]}")
		scores[resultat - 1][1] = 3

		if (resultat - 1) == 0:
			scores[1][1] = 1
		else:
			scores[0][1] = 1


	return scores