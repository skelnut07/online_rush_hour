car_dict = {
    "O": [0, [2, 3], 0],
    "R": [2, [1, 1], 1],
    "W": [2, [6, 2], 1],
    "L": [3, [5, 2], 0],
    "D": [2, [3, 0], 1],
    "P": [3, [2, 2], 0]}
BOARDSIZE = 7


def get_car_coords(location, direction, length):
    cords = []
    y = location[0]
    x = location[1]
    if direction == 0:
        for num in range(length):
            cords.append((y, location[1]))
            y += 1
    else:
        for num in range(length):
            cords.append((location[0], x))
            x += 1
    return cords


def board_coordinates():
    cords = set()
    for col in range(BOARDSIZE):
        for lin in range(BOARDSIZE):
            cords.add((col, lin))
    cords.add(int(BOARDSIZE / 2))
    return cords


def create_starter_board():
    board = []
    for num in range(BOARDSIZE):
        smaller_list = ["_" for num in range(BOARDSIZE)]
        board.append(smaller_list)

    board[int(BOARDSIZE / 2)].append("_")
    return board


# "O":[0,[2,3],0],
def add_car(board, carkey, car_info, cars):
    cords = get_car_coords(car_info[1], car_info[2], car_info[0])
    work = 0
    is_cord = 0
    board_cords = board_coordinates()
    for i in cords:
        if i in board_cords:
            is_cord += 1
    if is_cord == len(cords):
        for cord in cords:
            if board[cord[0]][cord[1]] == "_":
                work += 1
        if work == len(cords):
            for i in range(len(cords)):
                board[(cords[i][0])][(cords[i][1])] = carkey
            cars[carkey] = car_info
            return board, cars
    return board, cars


def load_board(cars_dict):
    board = create_starter_board()
    current_cars = {}
    for carkey in cars_dict:
        added_car = add_car(board, carkey, cars_dict[carkey], current_cars)
        board, current_cars = added_car[0], added_car[1]
    return board


loaded_board = load_board(car_dict)
print('\n'.join(map(str, loaded_board)))
