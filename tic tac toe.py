def print_board(board):
  """Prints the current state of the Tic-Tac-Toe board."""
  for row in board:
    print("  ".join(row))
  print()

def check_win(board):
  """Checks if there's a winner on the board."""
  # Check rows
  for row in board:
    if row[0] == row[1] == row[2] and row[0] != '-':
      return row[0]
  # Check columns
  for col in range(3):
    if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '-':
      return board[0][col]
  # Check diagonals
  if (board[0][0] == board[1][1] == board[2][2] or
      board[0][2] == board[1][1] == board[2][0]) and board[1][1] != '-':
    return board[1][1]
  # No winner yet
  return None

def is_board_full(board):
  """Checks if the board is full."""
  for row in board:
    for cell in row:
      if cell == '-':
        return False
  return True

def get_player_move(player):
  """Gets the player's move."""
  while True:
    try:
      row, col = map(int, input(f"Player {player}, enter your move (row, col) from 1-3: ").split(","))
      if 1 <= row <= 3 and 1 <= col <= 3:
        return row - 1, col - 1
      else:
        print("Invalid input. Row and column must be between 1 and 3.")
    except ValueError:
      print("Invalid input. Please enter two numbers separated by a comma.")

def play_tic_tac_toe():
  """Main function to play Tic-Tac-Toe."""
  board = [['-' for _ in range(3)] for _ in range(3)]
  current_player = 'X'
  winner = None

  while winner is None and not is_board_full(board):
    print_board(board)
    row, col = get_player_move(current_player)

    if board[row][col] == '-':
      board[row][col] = current_player
      winner = check_win(board)
      current_player = 'O' if current_player == 'X' else 'X'
    else:
      print("That spot is already taken. Try again.")

  print_board(board)
  if winner:
    print(f"Player {winner} wins!")
  else:
    print("It's a tie!")

if __name__ == "__main__":
  play_tic_tac_toe()