from copy import deepcopy
def find_check(king_pos, king_color, board):
    x = king_pos[0]
    y = king_pos[1]

    # horizontal check (covers queen and rook)
    x = x+1
    while x <= 7 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == "queen" or p.piece_type == "rook":
            return True
        x += 1
    x = king_pos[0] - 1
    while x >= 0 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == "queen" or p.piece_type == "rook":
            return True
        x -= 1

    # vertical check (covers queen and rook)
    x = king_pos[0]
    y = king_pos[1] + 1
    while y <= 7 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == "queen" or p.piece_type == "rook":
            return True
        y += 1
    y = king_pos[1] - 1
    while y >= 0 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == "queen" or p.piece_type == "rook":
            return True
        y -= 1

    # diagonal
    x = king_pos[0] + 1
    y = king_pos[1] + 1
    while x <= 7 and y <= 7 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == 'bishop':
            return True
        elif p.piece_type == "pawn":
            if abs(x - king_pos[0]) == 1 and (y-king_pos[1] == 1):
                return True
        x += 1
        y += 1

    x = king_pos[0] - 1
    y = king_pos[1] + 1
    while x <= 7 and y <= 7 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == 'bishop':
            return True
        elif p.piece_type == "pawn":
            if abs(x - king_pos[0]) == 1 and (y - king_pos[1] == 1):
                return True
        x -= 1
        y += 1

    x = king_pos[0] - 1
    y = king_pos[1] - 1
    while x <= 7 and y <= 7 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == 'bishop':
            return True
        elif p.piece_type == "pawn":
            if abs(x - king_pos[0]) == 1 and (y - king_pos[1] == 1):
                return True
        x -= 1
        y -= 1

    x = king_pos[0] + 1
    y = king_pos[1] - 1
    while x <= 7 and y <= 7 and board.getPiece([x, y]).color != king_color:
        p = board.getPiece([x, y])
        if p == "":
            continue
        elif p.piece_type == 'bishop':
            return True
        elif p.piece_type == "pawn":
            if abs(x - king_pos[0]) == 1 and (y - king_pos[1] == 1):
                return True
        x += 1
        y -= 1

    x = king_pos[0]
    y = king_pos[1]
    # knight check
    knight_check_list = [
        [y + 1, x + 3], [y + 1, x - 3], [y - 1, x + 3], [y - 1, x - 3],
        [x + 1, y + 3], [x + 1, y - 3], [x - 1, y + 3], [x - 1, y - 3]
    ]
    for pos in knight_check_list:
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            p = board.getPiece(pos)
            if p.piece_type == "knight" and p.color != king_color:
                return True

    return False

def find_checkmate(king_pos, king_color, board):
    x = king_pos[0]
    y = king_pos[1]

    open_spaces = []
    possible_os = [
        [x + 1, y], [x+1, y+1], [x, y+1],
        [x-1, y+1], [x-1, y], [x-1, y-1],
        [x, y-1], [x+1, y-1]
    ]
    for pos in possible_os:
        if 0<=pos[0] <= 7 and 0 <= pos[1] <= 7:
            p = board.getPiece(pos)
            if p == "":
                open_spaces.append(pos)

    for pos in open_spaces:
        sim_board = deepcopy(board)
        sim_board.updateBoard(king_pos, pos)
        c = find_check(pos, king_color, sim_board)
        if not c:
            return True

    return False