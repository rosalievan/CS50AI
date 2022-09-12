import sys

from crossword import *
import math


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            for domain_item in self.domains[variable].copy():
                if variable.length != len(domain_item):
                    self.domains[variable].remove(domain_item)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        domain_was_updated = False
        overlaps = self.crossword.overlaps[x, y]

        if overlaps:
            for x_domain_item in self.domains[x].copy():
                possible_value_exists = False
                x_letter = x_domain_item[overlaps[0]]

                for y_domain_item in self.domains[y]:
                    y_letter = y_domain_item[overlaps[1]]
                    if x_letter == y_letter:
                        possible_value_exists = True
                
                if not possible_value_exists:
                    self.domains[x].remove(x_domain_item)
                    domain_was_updated = True

        return domain_was_updated
                  
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            arcs = []
            for x_variable in self.crossword.variables:
                for y_variable in self.crossword.variables:
                    if x_variable != y_variable:
                        arcs.append((x_variable, y_variable))
        
        empty_domain = True
        while arcs:
            x,y = arcs.pop(0)
            revision = self.revise(x,y)

            if revision:
                neighbors = self.crossword.neighbors(x)
                for y_variable in neighbors:
                    arcs.append((x, y_variable))

                if not self.domains[x]:
                    empty_domain = False
        
        return empty_domain

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        is_assignment_complete = True

        all_variables = list(self.crossword.variables)

        for variable in all_variables:
            if variable not in assignment:
                is_assignment_complete = False
        
        return is_assignment_complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        values_in_assignment = []

        for value in assignment.values():
            if value in values_in_assignment:
                return False
            values_in_assignment.append(value)

        for key in assignment:
            if key.length != len(assignment[key]):
                return False
        
        for var1 in assignment:
            neighbors = self.crossword.neighbors(var1)
            for var2 in neighbors:
                overlap= self.crossword.overlaps[var1, var2]
                if var2 in assignment:
                    if assignment[var1][overlap[0]] != assignment[var2][overlap[1]]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        dict = {}
        list = []
        if var not in assignment:
            for value in self.domains[var]:
                list.append(value)
                dict[value] = 0
                for neighbor in self.crossword.neighbors(var):
                    if neighbor not in assignment:
                        overlap = self.crossword.overlaps[var, neighbor]
                        for neighbor_value in self.domains[neighbor]:
                            if value[overlap[0]] != neighbor_value[overlap[1]]:
                                dict[value] += 1
        
        list = sorted(list, key=dict.get)

        return list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining_values_dict = {}
        for variable in self.crossword.variables:
            if variable not in assignment:
                remaining_values_dict[variable] = len(self.domains[variable])
        
        min_value = math.inf
        return_key = 0
        possible_keys = set()
        for key in remaining_values_dict:
            if remaining_values_dict[key] == min_value:
                possible_keys.add(return_key)
                possible_keys.add(key)
            elif remaining_values_dict[key] < min_value:
                return_key = key
                possible_keys = []

        degree_dict = {}
        if possible_keys:
            for key in possible_keys:
                degree_dict[key] = len(self.crossword.neighbors(key))
        
            return max(degree_dict)
        
        if not possible_keys:
            return return_key
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment1 = assignment.copy()
            assignment1[variable] = value

            if self.consistent(assignment1):
                assignment[variable] = value
                result = self.backtrack(assignment)
                if self.consistent(assignment):
                    return result

                assignment.remove(variable)
        
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
