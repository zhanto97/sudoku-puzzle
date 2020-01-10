from easy_puzzles import easy_puzzles
from medium_puzzles import medium_puzzles
from hard_puzzles import hard_puzzles
import random

class Board:
    def __init__(self, difficulty):
        if not difficulty in ['easy', 'medium', 'hard']:
            raise ValueError("difficulty can be 'easy', 'medium' or 'hard'")

        if difficulty == 'easy':
            self.board = random.choice(easy_puzzles)
        elif difficulty == 'medium':
            self.board = random.choice(medium_puzzles)
        else:
            self.board = random.choice(hard_puzzles)
        
        self.size = 9
        self.block = 3 # sqrt(9)
    
    def find_empty(self):
        """Finds an empty cell if exists.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def check_row(self, row, num):
        for j in range(self.size):
            if self.board[row][j] == num:
                return False
        return True
    
    def check_col(self, col, num):
        for i in range(self.size):
            if self.board[i][col] == num:
                return False
        return True

    def check_block(self, pos, num):
        x = pos[0] // self.block
        y = pos[1] // self.block

        for i in range(x*self.block, x*self.block + 3):
            for j in range(y*self.block, y*self.block + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def is_valid(self, pos, num):
        """Checks whether number NUM can be placed
        at position POS.
        """
        return self.check_row(pos[0], num) and \
               self.check_col(pos[1], num) and \
               self.check_block(pos, num)

    def solve(self):
        """Solves sudoku puzzle using backtracking.
        """
        empty = self.find_empty()
        if empty == None:
            return True
        
        for num in range(1, self.size + 1):
            if self.is_valid(empty, num):
                self.board[empty[0]][empty[1]] = num

                if self.solve():
                    return True
                self.board[empty[0]][empty[1]] = 0
        return False
     
    def print_board(self):
        for i in range(self.size):
            if i%3 == 0:
                print("- " * 13)
            for j in range(self.size):
                if j%3 == 0:
                    print("| ", end = "")
                
                if j == self.size - 1:
                    print(self.board[i][j], end = " |\n")
                else:
                    print(self.board[i][j], end = " ")
        print("- " * 13)


b = Board('hard')
b.print_board()
b.solve()
print("Solved version")
b.print_board()