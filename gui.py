import pygame
import sudoku
import threading

class App:
    def __init__(self, difficulty):
        self.running = True
        self.size = self.width, self.height = 660, 800
        self.board = sudoku.Board(difficulty)
        self.initial = [[0 for i in range(self.board.size)]
                            for j in range(self.board.size)]
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.initial[i][j] = self.board.board[i][j]
        self.solution = self.board.copy()
        self.solution.solve()
    
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Sudoku')
        self.font = pygame.font.SysFont('Arial', 60)
        self.selected = None
        self.candidate = 0
        self.wrong_cell = None
        self.wrong_time = 0
        self.animating = False

    def finished(self):
        """Returns True if puzzle is solved. False otherwise
        """
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] != self.solution.board[i][j]:
                    return False
        return True

    def draw_cells(self):
        """Draws cells around numbers
        """
        cell = self.width // (self.board.size + 2)
        for i in range(self.board.size + 1):
            width = 2
            if i%3 == 0:
                width = 5
            pygame.draw.line(self.display, (0, 0, 0), (cell, cell + i*cell),
                (cell + cell*self.board.size, cell + i*cell), width)
            pygame.draw.line(self.display, (0, 0, 0), (cell + i*cell, cell),
                (cell + i*cell, cell + cell*self.board.size), width)
    
    def highlight_initial(self):
        """Fills initial puzzle number cells with dark grey
        """
        cell = self.width // (self.board.size + 2)
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.initial[i][j] != 0:
                    pygame.draw.rect(self.display, (169,169,169),
                        (cell + j*cell, cell + i*cell, cell, cell), 0)

    def highlight_selected(self):
        """Fills selected cell with light gray
        """
        cell = self.width // (self.board.size + 2)
        if self.selected:
            pygame.draw.rect(self.display, (220,220,220),
                        (cell + self.selected[1]*cell, cell + self.selected[0]*cell, 
                        cell, cell), 0)
    
    def highlight_wrong(self):
        """Fills the cell with red if incorrect number is provided
        """
        if self.wrong_cell:
            cell = self.width // (self.board.size + 2)
            ticks = pygame.time.get_ticks()
            if self.wrong_time + 2000 > ticks:
                pygame.draw.rect(self.display, (255, 0, 0),
                        (cell + self.wrong_cell[1]*cell, cell + self.wrong_cell[0]*cell, 
                        cell, cell), 0)
            else:
                self.wrong_cell = None
                self.wrong_time = 0

    def draw_animation(self):
        """Fills tried cells with light blue and places number when
        backtrack solution animation is taking place
        """
        if self.animating:
            cell = self.width // (self.board.size + 2)
            for i in range(self.board.size):
                for j in range(self.board.size):
                    if self.animation[i][j] != 0:
                        pygame.draw.rect(self.display, (153, 207, 224),
                            (cell + j*cell, cell + i*cell, cell, cell), 0)
                        text = self.font.render(str(self.animation[i][j]), True, (0, 0, 0))
                        rect = text.get_rect()
                        rect.center = (cell + j*cell + cell//2, cell + i*cell + cell//2)
                        self.display.blit(text, rect)

    def draw_numbers(self):
        """Draws numbers in respective cells
        """
        cell = self.width // (self.board.size + 2)
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] != 0:
                    text = self.font.render(str(self.board.board[i][j]), True, (0, 0, 0))
                    rect = text.get_rect()
                    rect.center = (cell + j*cell + cell//2, cell + i*cell + cell//2)
                    self.display.blit(text, rect)
    
    def draw_candidate(self):
        """Draws number user wants to input in cell
        """
        cell = self.width // (self.board.size + 2)
        if self.selected:
            if self.candidate:
                text = self.font.render(str(self.candidate), True, (0, 0, 0))
                rect = text.get_rect()
                rect.center = (cell + self.selected[1]*cell + cell//2,
                    cell + self.selected[0]*cell + cell//2)
                self.display.blit(text, rect)

    def draw_solve_button(self):
        """Draws "Solve" button on the bottom
        """
        cell = self.width // (self.board.size + 2)
        pygame.draw.rect(self.display, (0, 0, 0),
                        (cell + 3*cell, cell + 10*cell, 
                        3*cell, cell), 2)
        text = self.font.render("Solve", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (cell + 3*cell + int(cell*1.5),
            cell + 10*cell + cell//2)
        self.display.blit(text, rect)

    def find_cell_by_pos(self, pos):
        """Finds which cell is selected by mouse position POS
        """
        cell = self.width // (self.board.size + 2)
        if pos[0] < cell or pos[0] > cell + cell*self.board.size or \
            pos[1] < cell or pos[1] > cell + cell*self.board.size:
            return None
        x = pos[0] // cell
        y = pos[1] // cell
        return (y-1, x-1)
    
    def find_solve_button(self, pos):
        """Returns True if mouse is pressed on "Solve" button.
        False otherwise
        """
        cell = self.width // (self.board.size + 2)
        x = pos[0]
        y = pos[1]
        return cell + 10*cell < y and y < cell + 11*cell and \
            cell + 3*cell < x and x < cell * 6*cell

    def solve_animation(self):
        """Shows visualization of how backtracking
        solver solves the puzzle
        """
        if self.stop_thread:
            return False

        empty = self.board.find_empty()
        if empty == None:
            return True
        
        for num in range(1, self.board.size + 1):
            if self.board.is_valid(empty, num):
                self.animation[empty[0]][empty[1]] = num
                self.board.board[empty[0]][empty[1]] = num
                pygame.time.delay(50)

                if self.solve_animation():
                    return True
                
                self.board.board[empty[0]][empty[1]] = 0
                self.animation[empty[0]][empty[1]] = 0
                pygame.time.delay(50)
        return False

    def switcher(self, event_key):
        """Event key to local key mapping
        """
        switch = {
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 4,
            pygame.K_5: 5,
            pygame.K_6: 6,
            pygame.K_7: 7,
            pygame.K_8: 8,
            pygame.K_9: 9,
            pygame.K_DELETE: 0,
            pygame.K_RETURN: -1,
        }
        return switch.get(event_key, None)

    def on_event(self, event):
        """Decides which action to take on particular event
        """
        if event.type == pygame.QUIT:
            self.running = False
            if self.animating:
                self.stop_thread = True
                self.thread.join()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.animating:
                return
            pos = pygame.mouse.get_pos()
            board_pos = self.find_cell_by_pos(pos)
            if board_pos and self.initial[board_pos[0]][board_pos[1]] == 0:
                if self.selected != board_pos:
                    self.selected = board_pos
                    self.candidate = 0
            elif self.find_solve_button(pos):
                self.selected = None
                self.candidate = 0
                self.animating = True
                self.animation = [[0 for i in range(self.board.size)]
                            for j in range(self.board.size)]
                self.thread = threading.Thread(target=self.solve_animation)
                self.stop_thread = False
                self.thread.start()
            else:
                self.selected = None
                self.candidate = 0
        elif event.type == pygame.KEYDOWN:
            if self.animating:
                return
            key = self.switcher(event.key)
            if key == None:
                return

            if 0 <= key and key <= self.board.size:
                # Should change a bit to allow for boards
                # of bigger size
                self.candidate = key
            elif key == -1 and self.selected and self.candidate:
                x = self.selected[0]
                y = self.selected[1]
                if self.solution.board[x][y] == self.candidate:
                    self.board.board[x][y] = self.candidate
                    if self.selected == self.wrong_cell:
                        self.wrong_cell == None
                    self.selected = None
                    self.candidate = 0
                else:
                    ticks = pygame.time.get_ticks()
                    self.wrong_cell = (self.selected[0], self.selected[1])
                    self.wrong_time = ticks
                    self.candidate = 0

    def on_render(self):
        """Renders Sudoku puzzle on display
        """
        self.display.fill((255, 255, 255))
        self.highlight_initial()
        self.highlight_selected()
        self.highlight_wrong()
        self.draw_animation()
        self.draw_cells()
        self.draw_numbers()
        self.draw_candidate()
        self.draw_solve_button()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        try:
            self.on_init()
        except:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            
            if self.finished():
                self.running = False
                # print("Congratulations!")
        self.on_render()
        pygame.time.delay(1000)
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App('easy')
    theApp.on_execute()

