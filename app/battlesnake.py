import numpy as np

class CellState():
    SnakeHead = 0
    SnakeTail = 1
    Food = 2
    You = 3
    FirstSnakes = 4
    LastSnakes = 10
    MAX = LastSnakes + 1
OneHotStates = np.eye(CellState.MAX)

class Board():
    def __init__(self, data):
        board = data["board"]
        self.height = board["height"]
        self.width = board["width"]

        self.grid = np.zeros((self.width, self.height, CellState.MAX))

        self.you = Snake(data["you"])
        self.add_snake(self.you, CellState.You)

        i = CellState.FirstSnakes
        for snake in board["snakes"]:
            self.add_snake(Snake(snake), i)
            i += 1

        self.add_food(board["food"])

    def add_snake(self, snake, snake_id):
        for (x,y) in snake.body:
            self.grid[x][y] = self.grid[x][y] + OneHotStates[snake_id]

        (hx, hy) = snake.head
        self.grid[hx][hy] = self.grid[hx][hy] + OneHotStates[CellState.SnakeHead]

    def add_food(self, food):
        for coord in food:
            self.grid[coord["x"]][coord["y"]] = self.grid[coord["x"]][coord["y"]] + OneHotStates[CellState.Food]

    def display(self):
        print(self.grid.T)

class Snake():
    def __init__(self, snake_data):
        body = []
        for coord in snake_data["body"]:
            body.append((coord["x"], coord["y"]))
        self.body = body
        self.head = body[0]

    def safe_moves(self, board):
        (x,y) = self.head

        moves = { "left" : (x-1, y),
            "right" : (x+1, y),
            "up" : (x, y-1),
            "down" : (x, y+1),
        }

        valid_moves = []
        for (move, coord) in moves.items():
            (x, y) = coord
            if 0 <= x < board.width and 0 <= y < board.height:
                cell_state = board.grid[x][y]
                if not cell_state.any() or np.array_equal(cell_state, OneHotStates[CellState.Food]):
                    valid_moves.append(move)
        return valid_moves
