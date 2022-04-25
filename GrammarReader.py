#  Salah-eddine Niazi
import random
import re
import sys


def grammaire():
    return {'<S>': [['<visibilite>', '<fin_abs>', 'class', '<ID>', '<heritage>', '<interfaces>']],
            '<visibilite>': [[''], ['public'], ['protected']],
            '<fin_abs>': [[''], ['final'], ['abstract']],
            '<heritage>': [['extends', '<ID>']],
            '<interfaces>': [[''], ['implements', '<ID>', '<liste_i>']],
            '<liste_i>': [[''], [',', '<ID>', '<liste_i>']],
            '<ID>': [['JButton'], ['Object'], ['Main'], ['Exemple'], ['ArrayList'], ['IGraph'], ['IPhone'],
                     ['IMessage'], ['Parseur'], ['Grammar']]}


# fonction que j'ai defini pour enelever les " dans le token ansi que les \n de la syntaxe importé de gramais BNF
# fonction pour se debaarsser des " et des retours a la ligne
def cleanchaine(chaine):
    newchaine = []
    for c in chaine:
        if chaine == '"\n"':
            return '\n'
        if c != '"' and c != '\n' and c != '\t':
            newchaine.append(c)
    newchaine = "".join(newchaine)

    return newchaine


# fonction qui parse une grammaire d'un fichier bnf , elle retourne  la grammaire sous forme de dictionnaire si elle respect l'automate
def parseGrammaire(nomfichier):
    liste = []
    grammaire = dict()
    with open(nomfichier, "r") as file:
        for line in file:
            token = []
            token = line.split(' ')
            parse = parsetoken(token, grammaire)
            if parse == False:
                # grammaire ne respecte pas l'automate
                return False
            else:
                liste.append(parse)
    return grammaire


# FONCTION QUI DETERMINE LE TYPE DU TOKEN LU T ou NT ou epsilon ou symbol

def deftoken(mot):
    if (mot.startswith('\t') or mot.endswith('\t')):
        mot =cleanchaine(mot)

    if (mot.startswith('<') and mot.endswith('>')):
        return "NT"
    elif (mot.startswith('<') and mot.endswith('>\n')):
        return "NT"

    elif mot == "epsilon\n":
        return "epsilon"

    elif mot == "epsilon":
        return "epsilon"
    # ON TRAITE LES CAS PARTICULIER
    elif mot == "::=":
        return "::="

    elif mot == "|":
        return "|"

    elif (mot.startswith('"') and mot.endswith('"\n')):
        return "T"
    elif (mot.startswith('"') and mot.endswith('"')):
        return "T"


    else:
        # return False
        return "Non reconu"


# FONCTION QUI PERMET DE LIRE LES TOKEN RECUPERE DU FICHIER

def parsetoken(tokens, grammaire):
    liste = []
    expression = []

    machine = {"Q0": {"NT": "Q1"},
               "Q1": {"::=": "Q2"},
               "Q2": {"epsilon": "Q3", "T": "Q5", "NT": "Q5"},
               "Q3": {"|": "Q4"},
               "Q4": {"NT": "Q5", "T": "Q5"},
               "Q5": {"NT": "Q5", "T": "Q5", "|": "Q4"},

               }
    etat = "Q0"
    for token in tokens:
        transitions = machine[etat]

        if (deftoken(token) not in transitions.keys()):
            raise Exception("Erreur de Parsage:le token lu ne respecte pas l'automate ,token lu", token, "de type",
                            deftoken(token), "Token attendu", ",".join(machine[etat].keys()))
        etat = transitions[deftoken(token)]
        if etat == "Q1":
            key = token
            grammaire[key] = []

        elif etat == "Q3":
            # d'aprés l'enoncé on lit tjr epsilon en premier
            if deftoken(token) == "epsilon":
                a = ['']
                grammaire[key].append(a)
            elif deftoken(token) == "T" or deftoken(token) == "NT":
                if token.startswith('"\\n'):
                    # Caractére special , faut le traiter differement
                    token = '"\n"'
                expression.append(cleanchaine(token))
                # si le token se termine par \n c'est la fin de
                if token.endswith("\n"):
                    grammaire[key].append(expression)

        elif etat == "Q4":
            if deftoken(token) == "|":
                # fonction del et remove ne donne pas le resultat voulu alors j'ai choisi de faire autrement
                # RENITIALISER  la liste expression et tester si elle est vide avant de l'enregistrer
                if expression != []:
                    grammaire[key].append(expression)
                    expression = []
                # del expression[:]

        elif etat == "Q5":
            if deftoken(token) == "T" or deftoken(token) == "NT":
                if token.startswith('"\\n'):
                    token = '"\n"'
                expression.append(cleanchaine(token))
                if token.endswith("\n"):
                    grammaire[key].append(expression)

    if (etat in ["Q3", "Q5"]):
        return True

        # etats finaux
    else:
        return False


# FONCTION GENERE QUI GENERE UNE PHRASE D'UNE GRAMMAIRE ECRITE SOUS FORME DE dictionaire

def genere(grammaire):
    phrase = []

    def parser(grammaire, token, phrase):
        nonterminal = False

        for keys in grammaire.keys():
            if token == keys:
                nonterminal = True

        if nonterminal == True:
            return parser(grammaire, random.choice(grammaire[token]), phrase)

        elif type(token) is list:
            for value in token:
                parser(grammaire, value, phrase)
        else:

            phrase.append(token)
            return phrase

    token = '<S>'

    parser(grammaire, token, phrase)
    return " ".join(phrase)


# debut de programme

if __name__ == "__main__":
    # g = parseGrammaire("classDecl.bnf")

    print("--------------------------------Sur l'exemple Email Prof------------------------------------")
    #print("la grammaire generé est", parseGrammaire("emailProf.bnf"))
    print("--------------------------------------------------------------------------------------------")
    #print(genere(parseGrammaire("emailProf.bnf")))
    print("--------------------------------------------------------------------------------------------")
    print("---------------sur l'exemple de la fonction grammaire() qui retourne une gramaire-----------")
    print("La phrase generé a partir de la gramaire est : ", genere(grammaire()))
    print("--------------------------------------------------------------------------------------------")
    print("-----------------------------------sur le fichier classFecl.bnf-----------------------------")
    print("a partir du fichier : ", genere(parseGrammaire("classDecl.bnf")))
    print("la grammaire generé est", parseGrammaire("classDecl.bnf"))
    print("--------------------------------------------------------------------------------------------")
    print("----------------------------------------Type enumeration------------------------------------")
    print("a partir du fichier : ", genere(parseGrammaire("typEnum.bnf")))
    print("la grammaire generé est", parseGrammaire("typEnum.bnf"))
    print("--------------------------------------------------------------------------------------------")
