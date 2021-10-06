#-*-coding: utf8-*-
import string

class SudokuGrid:
    """Cette classe représente une grille de Sudoku.
    Toutes ces méthodes sont à compléter en vous basant sur la documentation fournie en docstring.
    """

    def __init__(self, initial_values_str):
        """À COMPLÉTER!
        Ce constructeur initialise une nouvelle instance de la classe SudokuGrid.
        Il doit effectuer la conversation de chaque caractère de la chaîne en nombre entier,
        et lever une exception (ValueError) si elle ne peut pas être interprétée comme une grille de Sudoku.
        :param initial_values_str: Une chaîne de caractères contenant **exactement 81 chiffres allant de 0 à 9**,
            où ``0`` indique une case vide
        :type initial_values_str: str
        """
        # initialisation variables & liste
        self.myList = []
        myLign = []
        i = 1

        # verification taille totale grille
        if len(initial_values_str) == 81:
        # boucle for gérant le remplissage des listes
            for a in range(len(initial_values_str)):
                try:
                    # conversion str en int
                    case = int(initial_values_str[a])
                    myLign.append(case)

                    # test si ligne complete cad 9 valeurs dans la liste myLign
                    if i == 9:
                        self.myList.append(myLign)
                        myLign = []
                        i = 0
                    i += 1
                except ValueError:
                    print("Le gameset ne doit uniquement être composé que de chiffres. (Value Error)")
                    raise
        else:
            print("Le gameset doit comporter exactement 81 chiffres.")
            raise ValueError

    @staticmethod
    def from_file(filename, line):
        """À COMPLÉTER!
        Cette méthode de classe (ou méthode statique) crée une nouvelle instance de grille de Sudoku
        à partir d'une ligne contenue dans un fichier.

        :param filename: Chemin d'accès vers le fichier à lire
        :param line: Numéro de la ligne à lire
        :type filename: str
        :type line: int
        :return: La grille de Sudoku correspondant à la ligne donnée dans le fichier donné
        :rtype: SudokuGrid
        """

        with open(filename, 'r') as file:
            for i in range(line):
                param = file.readline()
            for i in param:
                if i == "\n":
                    param = param[:-1]
        file.close()
        return SudokuGrid(str(param))


    @staticmethod
    def from_stdin():
        """À COMPLÉTER!
        Cette méthode de classe crée une nouvelle instance de grille de Sudoku
        à partir d'une ligne lu depuis l'entrée standard (saisie utilisateur).
        *Variante avancée: Permettez aussi de «piper» une ligne décrivant un Sudoku.*
        :return: La grille de Sudoku correspondant à la ligne donnée par l'utilisateur
        :rtype: SudokuGrid
        """
        param = input()
        SudokuGrid(str(param))

    def __str__(self):
        """À COMPLÉTER!
        Cette méthode convertit une grille de Sudoku vers un format texte pour être affichée.
        :return: Une chaîne de caractère (sur plusieurs lignes...) représentant la grille
        :rtype: str
        """
        textGrid = ""
        for i in range(9):
            temp = ""
            for j in range(9):
                temp += str(self.myList[i][j])
            textGrid += temp + "\n"

        return textGrid

    def get_row(self, i):
        """À COMPLÉTER!
        Cette méthode extrait une ligne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param i: Numéro de la ligne à extraire, entre 0 et 8
        :type i: int
        :return: La liste des valeurs présentes à la ligne donnée
        :rtype: list of int
        """
        listLign = []
        if i in range(9):
            listLign = (self.myList[i][colonne] for colonne in range(9))
        else:
            print("Veuillez entrer une ligne comprise dans [0;8]")

        return listLign

    def get_col(self, j):
        """À COMPLÉTER!
        Cette méthode extrait une colonne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param j: Numéro de la colonne à extraire, entre 0 et 8
        :type j: int
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of int
        """
        listColumn = []
        if j in range(9):
            listColumn = (self.myList[ligne][j] for ligne in range(9))
        else:
            print("Veuillez entrer une ligne comprise dans [0;8]")

        return listColumn

    def get_region(self, reg_row, reg_col):
        """À COMPLÉTER!
        Cette méthode extrait les valeurs présentes dans une région donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param reg_row: Position verticale de la région à extraire, **entre 0 et 2**
        :param reg_col: Position horizontale de la région à extraire, **entre 0 et 2**
        :type reg_row: int
        :type reg_col: int
        :return: La liste des valeurs présentes à la région donnée
        :rtype: list of int
        """
        listReg = []
        # test valeurs renseignees en params
        if reg_row in range(3) and reg_col in range(3):
            # on itère maintenant sur i et j afin de remplir une liste contenant la région souhaitée
            listReg = (self.myList[i + reg_row * 3][j + reg_col * 3] for i in range(3) for j in range(3))
        else:
            print("Veuillez entrer des positions de région comprises dans [0;2]")

        return listReg

    def get_empty_positions(self):
        """À COMPLÉTER!
        Cette méthode renvoit les positions des cases vides dans la grille de Sudoku,
        sous la forme de tuples ``(i,j)`` où ``i`` est le numéro de ligne et ``j`` le numéro de colonne.
        *Variante avancée: Renvoyez un générateur sur les tuples de positions ``(i,j)`` au lieu d'une liste*
        :return: La liste des positions des cases vides dans la grille
        :rtype: list of tuple of int
        """
        """ listCoord = []
        coord = (0, 0)
        for i in range(9):
            for j in range(9):
                if self.myList[i][j] == 0:
                    listCoord.append((i, j))"""
        listCoord = ((i, j) for i in range(9) for j in range(9) if self.myList[i][j] == 0)

        return listCoord

    def write(self, i, j, v):
        """À COMPLÉTER!
        Cette méthode écrit la valeur ``v`` dans la case ``(i,j)`` de la grille de Sudoku.
        *Variante avancée: Levez une exception si ``i``, ``j`` ou ``v``
        ne sont pas dans les bonnes plages de valeurs*
        *Variante avancée: Ajoutez un argument booléen optionnel ``force``
        qui empêche d'écrire sur une case non vide*
        :param i: Numéro de ligne de la case à mettre à jour, entre 0 et 8
        :param j: Numéro de colonne de la case à mettre à jour, entre 0 et 8
        :param v: Valeur à écrire dans la case ``(i,j)``, entre 1 et 9
        """
        if i in range(9) and j in range(9) and v in range(1, 10) and (self.myList[i][j] == 0):
            self.myList[i][j] = v

    def copy(self):
        """À COMPLÉTER!
        Cette méthode renvoie une nouvelle instance de la classe SudokuGrid,
        qui doit être une copie **indépendante** de la grille de Sudoku.
        *Variante avancée: vous pouvez utiliser ``self.__new__(self.__class__)``
        pour court-circuiter l'appel à ``__init__`` et manuellement initialiser les attributs de la copie.*
        :return: Une copie de la grille courrante
        :rtype: SudokuGrid
        """
        copyGrid = [[self.myList[i][j] for j in range(9)] for i in range(9)]
        new_grid = self.__new__(self.__class__)
        new_grid.myList = copyGrid

        return new_grid
