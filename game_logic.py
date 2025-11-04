
def initialize_board():
    return [" " for _ in range(9)]

def display_board(board):
    for i in range(3):
        print(f'{board[0]} || {board[1]} || {board[2]} ||')
        print(f'{board[3]} || {board[4]} || {board[5]} ||')
        print(f'{board[6]} || {board[7]} || {board[8]} ||')

def check_winner(board):
    winning_combos= [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in winning_combos:
        
        if board[a] == board[b] == board[c] != " ":
            return board[a]
        if " " not in board:
            return "tie"

    return None