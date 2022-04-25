

import sys

def parseNombre(caracteres):
	print("parsage de:"+caracteres)
	tokens =[]
	for car in caracteres:
		tokens.append(lex(car))
	return parseTokens(tokens)

def lex(car):
	#unités lexicales:
	if (car=='0'):
		return ('0', 0)
	elif (car>'0' and car<='9'):
		return ('[1-9]', int(car))
	elif (car=='.'):
		return ('.', '.')
	raise Exception("Erreur lexicale: caractère trouvé:"+ car + '|')

def parseTokens(tokens):
	"""
	parse un nombre sous la forme 0 ou 46 ou 0.004 ou 1.23 ou 987.34
	"""
	#definition de l'automate / la machine a etats
	print("tokens:",tokens)
	machine = { "Q0": {	"0":"Q2", "[1-9]":"Q1"},
				"Q1": {"0":"Q1", "[1-9]":"Q1", ".":"Q3"},
				"Q2": {".":"Q3"},
				"Q3": {"0":"Q4", "[1-9]": "Q4"},
				"Q4": {"0":"Q4", "[1-9]": "Q4"}
				}
	nombre = 0
	diviseur = 1
	etat = "Q0"
	print("nombre = 0")
	while(len(tokens)>0): # tant qu'il reste des token
		tok = tokens.pop(0)
		transitions = machine[etat]
		if(tok[0] not in transitions.keys()): #le caractère rencontré n'est pas accepté dans cet état
			raise Exception("Erreur de Parsage: caractère trouvé:"+str(tok)+"; attendus:" + ",".join(machine[etat].keys()))
		etat=transitions[tok[0]]
		#nouvel état:
		if (etat == "Q1"): 
			nombre = nombre * 10 + tok[1] #on multiplie le nombre par 10 et on rajoute le nouveau chiffre comme chiffre des unités
			print ("*10 +", tok[1])
		#if (etat=="Q2"): rien à faire, nombre vaut 0
		# if (etat == "Q3"): rien à faire on vient de lire le point décimal
		elif (etat=="Q4"): # un autre chiffre apres la virgule
			#apres_virgule=apres_virgule+1 #incrémenter le décalage depuis le point décimal
			diviseur = diviseur*10 #puissances de 10
			valeurDec = tok[1]/diviseur
			nombre = nombre + valeurDec # on ajoute le chiffre avec le bon exposant
			print ("+", valeurDec)
	#sortie de boucle: on a terminé de parser le nombre			
	if (etat in ["Q1", "Q2","Q4"]): #etats finaux
		return nombre
	raise Exception("Erreur de Parsage: fin de ligne innattendue")

if __name__ == "__main__":
	print(parseNombre(sys.argv[1])) #parse le string passé en argument. Exemple: python3 parseurNombres.py 451.094






