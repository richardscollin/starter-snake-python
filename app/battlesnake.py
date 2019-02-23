import numpy as np

class CellState():
    SnakeHead = 0
    SnakeTail = 1
    Food = 2
    You = 3
    LargerHeads = 4
    FirstSnakes = 5
    LastSnakes = 13
    MAX = LastSnakes + 1

class Board():
    def __init__(self, data):
        board = data["board"]
        self.height = board["height"]
        self.width = board["width"]

        self.grid = np.zeros((self.width, self.height, CellState.MAX))

        self.you = Snake(data["you"])
        self.add_snake(self.you, CellState.You)

        i = CellState.FirstSnakes
        self.enemies = []
        for snake in board["snakes"]:
            enemy = Snake(snake)
            self.enemies.append(enemy)
            self.add_snake(enemy, i)
            i += 1

        self.add_food(board["food"])

    def add_snake(self, snake, snake_id):
        for (x,y) in snake.body:
            self.grid[x][y][snake_id] = 1

        (hx, hy) = snake.head
        self.grid[hx][hy][CellState.SnakeHead] = 1

        (hx, hy) = snake.tail
        self.grid[hx][hy][CellState.SnakeTail] = 1

    def add_food(self, food):
        for coord in food:
            self.grid[coord["x"]][coord["y"]][CellState.Food] = 1

    def display(self):
        print(self.grid.T)

class Snake():
    def __init__(self, snake_data):
        body = []
        for coord in snake_data["body"]:
            body.append((coord["x"], coord["y"]))
        self.body = body
        self.head = body[0]
        self.tail = body[-1]
        self.length = len(body)

    def get_movements(self, coord):
        (x,y) = coord

        return { "left" : (x-1, y),
            "right" : (x+1, y),
            "up" : (x, y-1),
            "down" : (x, y+1),
        }

    def safe_moves(self, board):
        moves = self.get_movements(self.head)

        larger_enemies = [x for x in board.enemies if x.length >= self.length]
        for enemy in larger_enemies:  # mark board around heads of larger enemy snakes
            if enemy.head != self.head:
                for coord in self.get_movements(enemy.head).values():
                    (x, y) = coord
                    if 0 <= x < board.width and 0 <= y < board.height:
                        board.grid[x][y][CellState.LargerHeads] = 1

        valid_moves = []
        for (move, coord) in moves.items():
            (x, y) = coord
            if 0 <= x < board.width and 0 <= y < board.height:
                cell_state = board.grid[x][y]
                if not cell_state.any() or cell_state[CellState.Food] or cell_state[CellState.SnakeTail]:
                    valid_moves.append(move)
        return valid_moves
