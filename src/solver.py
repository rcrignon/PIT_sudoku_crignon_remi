# -*-coding: utf8-*-
import operator
from grid import *

class SudokuSolver:
    """Cette classe permet d'explorer les solutions d'une grille de Sudoku pour la résoudre.
    Elle fait intervenir des notions de programmation par contraintes
    que vous n'avez pas à maîtriser pour ce projet."""

    def __init__(self, grid):
        """À COMPLÉTER
        Ce constructeur initialise une nouvelle instance de solver à partir d'une grille initiale.
        Il construit les ensembles de valeurs possibles pour chaque case vide de la grille,
        en respectant les contraintes définissant un Sudoku valide.
        Ces contraintes seront appliquées en appelant la méthode ``reduce_all_domains``.
        :param grid: Une grille de Sudoku
        :type grid: SudokuGrid
        """
        self.solutions = []
        self.grid = grid
        self.reduce_all_domains()

    def reduce_all_domains(self):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """
        for element in self.grid.get_empty_positions():
            liste_valeurs_possibles = set()
            ligne_tuple = list(self.grid.get_row(element[0]))
            colonne_tuple = list(self.grid.get_col(element[1]))
            region_tuple = list(self.grid.get_region(element[0] // 3, element[1] // 3))

            for i in range(1, 10):
                if i not in ligne_tuple and i not in colonne_tuple and i not in region_tuple:
                    liste_valeurs_possibles.add(i)

            self.solutions.append((element, liste_valeurs_possibles))

    def reduce_domains(self, last_i, last_j, last_v):
        """À COMPLÉTER
        Cette méthode devrait être appelée à chaque mise à jour de la grille,
        et élimine la dernière valeur affectée à une case
        pour toutes les autres cases concernées par cette mise à jour (même ligne, même colonne ou même région).
        :param last_i: Numéro de ligne de la dernière case modifiée, entre 0 et 8
        :param last_j: Numéro de colonne de la dernière case modifiée, entre 0 et 8
        :param last_v: Valeur affecté à la dernière case modifiée, entre 1 et 9
        :type last_i: int
        :type last_j: int
        :type last_v: int
        """
        for element in self.solutions:
            region_element = (element[0][0] // 3, element[0][1] // 3)
            region_last = (last_i // 3, last_j // 3)
            if last_v in element[1] and (
                    element[0][0] == last_i or element[0][1] == last_j or (region_element == region_last)):
                element[1].remove(last_v)

    def commit_one_var(self):
        """À COMPLÉTER
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """
        infos = ()
        for element in self.solutions:
            if len(element[1]) == 1:
                self.grid.write(element[0][0], element[0][1], next(iter(element[1])))
                infos = (element[0][0], element[0][1], next(iter(element[1])))
                return infos

        return None

    def solve_step(self):
        """À COMPLÉTER
        Cette méthode alterne entre l'affectation de case pour lesquelles il n'y a plus qu'une possibilité
        et l'élimination des nouvelles valeurs impossibles pour les autres cases concernées.
        Elle répète cette alternance tant qu'il reste des cases à remplir,
        et correspond à la résolution de Sudokus dits «simple».
        *Variante avancée: en plus de vérifier s'il ne reste plus qu'une seule possibilité pour une case,
        il est aussi possible de vérifier s'il ne reste plus qu'une seule position valide pour une certaine valeur
        sur chaque ligne, chaque colonne et dans chaque région*
        """
        last_change = -1
        while last_change is not None:
            last_change = self.commit_one_var()
            if last_change is not None:
                self.reduce_domains(last_change[0], last_change[1], last_change[2])
                self.clean_solutions(last_change)
                last_change = ()
            else:
                pass

    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        for element in self.solutions:
            if element[1] != set():
                return True
            else:
                return False

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """
        solution_complete = False
        if not list(self.grid.get_empty_positions()):
            solution_complete = True

        return solution_complete

    def branch(self):
        """À COMPLÉTER
        Cette méthode sélectionne une variable libre dans la solution partielle actuelle,
        et crée autant de sous-problèmes que d'affectation possible pour cette variable.
        Ces sous-problèmes seront sous la forme de nouvelles instances de solver
        initialisées avec une grille partiellement remplie.
        *Variante avancée: Renvoyez un générateur au lieu d'une liste.*
        *Variante avancée: Un choix judicieux de variable libre,
        ainsi que l'ordre dans lequel les affectations sont testées
        peut fortement améliorer les performances de votre solver.*
        :return: Une liste de sous-problèmes ayant chacun une valeur différente pour la variable choisie
        :rtype: list of SudokuSolver
        """
        list_solutions = []
        coordonnees_mini = ()
        set_mini = {}
        self.solutions.sort(key=lambda oui: len(oui[1]))
        coordonnees_mini = self.solutions[0][0]
        set_mini = self.solutions[0][1]
        for i in set_mini:
            grille_sudoku_en_cours = self.grid.copy()
            grille_sudoku_en_cours.write(coordonnees_mini[0], coordonnees_mini[1], i)
            sous_probleme = self.__class__(grille_sudoku_en_cours)
            list_solutions.append(sous_probleme)

        return list_solutions

    def solve(self):
        """
        Cette méthode implémente la fonction principale de la programmation par contrainte.
        Elle cherche d'abord à affiner au mieux la solution partielle actuelle par un appel à ``solve_step``.
        Si la solution est complète, elle la retourne.
        Si elle est invalide, elle renvoie ``None`` pour indiquer un cul-de-sac dans la recherche de solution
        et déclencher un retour vers la précédente solution valide.
        Sinon, elle crée plusieurs sous-problèmes pour explorer différentes possibilités
        en appelant récursivement ``solve`` sur ces sous-problèmes.
        :return: Une solution pour la grille de Sudoku donnée à l'initialisation du solver
        (ou None si pas de solution)
        :rtype: SudokuGrid or None
        """
        self.solve_step()
        if self.is_solved():
            return self.grid
        elif self.is_valid():
            oui = self.branch()
            for element in oui:
                s = element.solve()
                if s is not None:
                    return s
            return None
        else:
            return None

    def clean_solutions(self, last_change):
        self.solutions.remove(((last_change[0], last_change[1]), set()))
