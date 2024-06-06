import tkinter as tk
from tkinter import messagebox
import math

# Function to check for a win
def check_win(board, player):
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_states

# Function to check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Function to get valid moves
def get_valid_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, "X"):
        return -1
    elif check_win(board, "O"):
        return 1
    elif check_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (r, c) in get_valid_moves(board):
            board[r][c] = "O"
            score = minimax(board, depth + 1, False)
            board[r][c] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in get_valid_moves(board):
            board[r][c] = "X"
            score = minimax(board, depth + 1, True)
            board[r][c] = " "
            best_score = min(score, best_score)
        return best_score

# Function to get the best move
def best_move(board):
    best_score = -math.inf
    move = None
    for (r, c) in get_valid_moves(board):
        board[r][c] = "O"
        score = minimax(board, 0, False)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

# Main game class
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c] = tk.Button(self.root, text=" ", font='Helvetica 20 bold', height=3, width=6,
                                               command=lambda r=r, c=c: self.on_button_click(r, c))
                self.buttons[r][c].grid(row=r, column=c)
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=3, column=1)

    def on_button_click(self, row, col):
        if self.board[row][col] == " " and self.current_player == "X":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X")
            if check_win(self.board, "X"):
                messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")
                self.reset_game()
            elif check_draw(self.board):
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O"
                self.computer_move()

    def computer_move(self):
        row, col = best_move(self.board)
        self.board[row][col] = "O"
        self.buttons[row][col].config(text="O")
        if check_win(self.board, "O"):
            messagebox.showinfo("Tic-Tac-Toe", "Player O wins!")
            self.reset_game()
        elif check_draw(self.board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            self.reset_game()
        else:
            self.current_player = "X"

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=" ")
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
