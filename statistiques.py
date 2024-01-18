from typing import Optional, TextIO

class StatistiqueJeu:
	# Le nom du jeu
	nomJeu: str

	# La liste du temps par joueur par coup
	temps: list[list[float]]

	# Si la valeur est -1, c'est une égalité, si 0 le robot qui joue en premier a gagné, si 1 le robot qui joue en deuxième a gagné
	victoire: Optional[int]

	# Non obligatoire, si c'est par rapport à une valeur particulière, on doit le préciser
	valeurParticuliere: Optional[float]

	difficultes: list[str]


def GenererFichierCSV(statistiques: list[StatistiqueJeu]) -> None:
	# Prends en argument une liste de statistiques et affiche dans le terminal un fichier CSV correspond aux statistiques
	# Attention, la longueur de temps[joueurId] doit être la même pour tous les joueurs et égal à la longueur de victoire

	contenuFichier: str
	statistique: StatistiqueJeu
	compteurA: int
	sommeCoupA: float
	sommeCoupB: float
	avecVictoires: bool
	avecValParticuliere: bool
	fichierCSV: TextIO


	contenuFichier = "Id; Nom du jeu; Difficulte joueur 0; Difficule joueur 1; Temps joueur 0; Temps joueur 1; Nombre de coups joueur 0; Nombre de coups joueur 1;"
	
	avecVictoires = False
	avecValParticuliere = False
	compteurA = 0
	while compteurA < len(statistiques) and (not avecVictoires or not avecValParticuliere) :
		statistique = statistiques[compteurA]

		if statistique.victoire != None:
			avecVictoires = True

		if statistique.valeurParticuliere is not None:
			avecValParticuliere = True

		compteurA += 1
	
	if avecVictoires:
		contenuFichier += "Victoire;"
	elif avecValParticuliere:
		contenuFichier += "Valeur particuliere;"


	compteurA = 0
	while compteurA < len(statistiques):
		statistique = statistiques[compteurA]

		contenuFichier += f"\n{compteurA + 1};{statistique.nomJeu};"
		contenuFichier += f"{statistique.difficultes[0]};{statistique.difficultes[1]};"

		sommeCoupA = 0
		sommeCoupB = 0

		for tempsA in statistique.temps[0]:
			sommeCoupA += tempsA
			
		for tempsB in statistique.temps[1]:
			sommeCoupB += tempsB

		contenuFichier += f"{sommeCoupA};{sommeCoupB};"
		contenuFichier += f"{len(statistique.temps[0])};{len(statistique.temps[1])};"

		if statistique.victoire is not None:
			contenuFichier += f"{statistique.victoire};"

		if statistique.valeurParticuliere is not None:
			contenuFichier += f"{statistique.valeurParticuliere};"

		
		compteurA += 1
	
	# On enregistre les statistiques dans un fichier csv appelé statistiques.csv
	fichierCSV = open("statistiques.csv", "w")
	fichierCSV.write(contenuFichier)
	fichierCSV.close()
