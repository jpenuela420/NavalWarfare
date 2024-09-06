def clear_screen():
    # Function to clear the screen by simulating a "clear" by printing multiple blank lines
    print("\n" * 50)

def print_board(board, hide_ships=False, owner=""):
    # Displays the board with a header indicating whose board it is and a format warning
    print("Do not use incorrect formats like (c11, 4a). Use the correct format (e.g., D2).")
    print(f"{owner}'s board, find their ship")
    print("    A   B   C   D   E")  # Column headers
    print("  +---+---+---+---+---+")
    for i, row in enumerate(board, start=1):
        # Hide ships if hide_ships is True, changing 'S' to blank spaces
        row_display = [' ' if cell == 'S' and hide_ships else cell for cell in row]
        print(f"{i} | {' | '.join(row_display)} |")  # Print the row with separators
        print("  +---+---+---+---+---+")

def update_board(board, row, col):
    # Updates the board by placing a ship 'S' if the position is empty
    if board[row][col] == ' ':
        board[row][col] = 'S'
        return True
    else:
        print("That position is already occupied. Try again.")
        return False

def is_valid_guess(board, row, col, guesses):
    # Checks if a guess is valid, ensuring it hasn't been guessed before
    if (row, col) in guesses:
        print("You have already guessed that position. Try again.")
        return False
    if board[row][col] == 'X' or board[row][col] == 'O':
        print("That position has already been guessed. Try again.")
        return False
    return True

def input_to_coords(input_str):
    # Converts user input (e.g., 'D2') into matrix coordinates
    col_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    # Checks that the input has at least two characters and that the column is valid
    if len(input_str) < 2 or input_str[0].upper() not in col_map:
        print("Invalid input. Use the correct format (e.g., D2).")
        return None, None
    try:
        row = int(input_str[1:]) - 1  # Converts the numeric part to a row index
        col = col_map[input_str[0].upper()]  # Maps the letter to a column index
        # Validate that the row is between 0 and 4 (equivalent to rows 1-5 in user input)
        if row < 0 or row > 4:
            print("The row must be between 1 and 5.")
            return None, None
        return row, col
    except (IndexError, ValueError, KeyError):
        # Handles any error if the conversion fails
        print("Invalid input. Use the correct format (e.g., D2).")
        return None, None

def update_score(score, player):
    # Increases the current player's score
    score[player] += 1
    return score

def hide_ships(board, player):
    # Allows players to hide their ships on their board
    for _ in range(5):
        while True:
            clear_screen()
            print_board(board, hide_ships=True)  # Shows the board hiding ships
            print(f"{player}, hide your ship (e.g., D2):")
            ship_input = input()  # User input for ship position
            ship_row, ship_col = input_to_coords(ship_input)
            # Checks if the input is valid and if the board update is successful
            if ship_row is not None and ship_col is not None and update_board(board, ship_row, ship_col):
                break

def play_game():
    # Initializes the score and players' boards
    score = {'Player 1': 0, 'Player 2': 0}
    boards = {
        'Player 1': [[' ' for _ in range(5)] for _ in range(5)],
        'Player 2': [[' ' for _ in range(5)] for _ in range(5)]
    }
    guesses = {'Player 1': set(), 'Player 2': set()}  # Keeps track of guesses

    # Players hide their ships
    hide_ships(boards['Player 1'], 'Player 1')
    hide_ships(boards['Player 2'], 'Player 2')

    # Main game loop
    current_player = 'Player 1'
    opponent = 'Player 2'

    while True:
        clear_screen()
        # Shows the opponent's board to the current player with hidden ships
        print_board(boards[opponent], hide_ships=True, owner=opponent)
        print(f"Score: Player 1 - {score['Player 1']}, Player 2 - {score['Player 2']}")
        print(f"{current_player}, guess the opponent's ship location (e.g., D2):")
        guess_input = input()  # Player input for guessing
        guess_row, guess_col = input_to_coords(guess_input)

        if guess_row is None or guess_col is None:
            # Continues if the input is invalid
            input("Press Enter to continue...")
            continue

        # Checks if the guess is valid
        if not is_valid_guess(boards[opponent], guess_row, guess_col, guesses[current_player]):
            input("Press Enter to continue...")
            continue

        guesses[current_player].add((guess_row, guess_col))  # Adds the guess to the record

        # Checks if the player hit a ship
        if boards[opponent][guess_row][guess_col] == 'S':
            print(f"{current_player} guessed correctly!")
            score = update_score(score, current_player)  # Updates the score
            boards[opponent][guess_row][guess_col] = 'X'  # Marks the hit on the board
        else:
            boards[opponent][guess_row][guess_col] = 'O'  # Marks a miss on the board
            print("You missed!")

        # Checks if a player has won
        if score[current_player] == 3:
            print(f"{current_player} wins!")
            break

        # Switches turns between players
        current_player, opponent = opponent, current_player
        input("Press Enter to switch turns...")

# Starts the game
play_game()