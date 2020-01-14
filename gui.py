import pygame
import sudoku

class App:
    def __init__(self, difficulty):
        self.running = True
        self.size = self.width, self.height = 660, 750
        self.board = sudoku.Board(difficulty)
        self.initial = [[0 for i in range(self.board.size)]
                            for j in range(self.board.size)]
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.initial[i][j] = self.board.board[i][j]
        self.board.print_board()
        self.solution = self.board.copy()
        self.solution.solve()
    
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Sudoku')
        self.font = pygame.font.SysFont('Arial', 60)
        self.draw_blocks()

    def draw_blocks(self):
        """Draws cells on canvas without numbers
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
        pygame.display.update()
    
    def highlight_initial(self):
        """Initial puzzle number blocks are filled with grey
        """
        cell = self.width // (self.board.size + 2)
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.initial[i][j] != 0:
                    pygame.draw.rect(self.display, (211,211,211),
                        (cell + j*cell, cell + i*cell, cell, cell), 0)
        pygame.display.update()
    
    def draw_numbers(self):
        """Draw numbers in blocks
        """
        cell = self.width // (self.board.size + 2)
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] != 0:
                    text = self.font.render(str(self.board.board[i][j]), True, (0, 0, 0))
                    rect = text.get_rect()
                    rect.center = (cell + j*cell + cell//2, cell + i*cell + cell//2)
                    self.display.blit(text, rect)
        pygame.display.update()

    def find_cell_by_pos(self, pos):
        cell = self.width // (self.board.size + 2)
        if pos[0] < cell or pos[0] > cell + cell*self.board.size or \
            pos[1] < cell or pos[1] > cell + cell*self.board.size:
            return None
        x = pos[0] // cell
        y = pos[1] // cell
        return (y-1, x-1)
    
    def switcher(self):
        switcher = {
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
            pygame.K_RETURN: -1
        }
        return switcher

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            board_pos = self.find_cell_by_pos(pos)
            if board_pos:
                self.selected = board_pos
        elif event.type == pygame.KEYDOWN:
            key = self.switcher().get(pygame.key, None)
            if key == None:
                return

            if 0 <= key and key <= self.board.size:
                # Should change a bit to allow for boards
                # of bigger size
                self.candidate = key
            elif key == -1:
                x = self.selected[0]
                y = self.selected[1]
                if self.solution.board[x][y] == self.candidate:
                    self.board.board[x][y] = self.candidate



    def on_loop(self):
        pass

    def on_render(self):
        self.display.fill((255, 255, 255))
        self.highlight_initial()
        self.draw_blocks()
        self.draw_numbers()


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
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App('easy')
    theApp.on_execute()

