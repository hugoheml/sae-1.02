from typing import Optional

class StatistiqueJeu:
	# Le nom du jeu
	nomJeu: str

	# La liste du temps pour chaque coups, par joueur, par manche
	temps: list[list[list[float]]]

	# Si la valeur est 0, le robot en facile à gagner sinon c'est le robot en difficile qui a gagné
	victoires: list[int]

	# Non obligatoire, si c'est par rapport à une valeur particulière, on doit le préciser
	valeurParticuliere: Optional[float]

	difficultes: list[str]


def GenererFichierCSV(statistiques: list[StatistiqueJeu]) -> None:
	# Prends en argument une liste de statistiques et affiche dans le terminal un fichier CSV correspond aux statistiques
	# Attention, la longueur de temps[joueurId] doit être la même pour tous les joueurs et égal à la longueur de victoire

	contenuFichier: str
	statistique: StatistiqueJeu
	compteurA: int
	compteurB: int
	sommeCoupA: float
	sommeCoupB: float

	contenuFichier = "Id; Nom du jeu; Difficulte joueur 0; Difficule joueur 1; Temps joueur 0; Temps joueur1; Nombre de coups joueur facile; Nombre de coups joueur difficile; Victoire; Valeur particulière;\n"
	print(contenuFichier)

	compteurA = 0
	while compteurA < len(statistiques):
		statistique = statistiques[compteurA]
		compteurB = 0

		while compteurB < len(statistique.temps[0]):
			contenuFichier += f"\n{compteurA + 1};{statistique.nomJeu};"
			contenuFichier += f"{statistique.difficultes[0]};{statistique.difficultes[1]};"

			sommeCoupA = 0
			sommeCoupB = 0

			for tempsA in statistique.temps[0][compteurB]:
				sommeCoupA += tempsA
				
			for tempsB in statistique.temps[1][compteurB]:
				sommeCoupB += tempsB

			contenuFichier += f"{sommeCoupA};{sommeCoupB};"
			contenuFichier += f"{len(statistique.temps[0][compteurB])};{len(statistique.temps[1][compteurB])};{statistique.victoires[compteurB]};"

			if statistique.valeurParticuliere is not None:
				contenuFichier += f"{statistique.valeurParticuliere};"

			compteurB += 1
		
		compteurA += 1

	print(contenuFichier)