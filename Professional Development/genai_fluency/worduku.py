import random
import re
import string
from nltk.corpus import words

def regex_matches_wordlist(regex, word_list):
    pattern = re.compile(regex)  # Compile the regex for efficiency
    for word in word_list:
        if pattern.fullmatch(word):  # Check for a full match
            return True
    return False

def generate_nine_character_words():
    word_list = words.words()  
    valid_words = [
        word for word in word_list if len(word) == 9 and len(set(word)) == 9
    ]
    return valid_words


def is_valid_letter(board, row, col, letter, valid_words):
    # Temporarily place the letter on the board
    board[row][col] = letter

    # Check the row
    row_word = "".join(board[row]).replace("0", ".")
    if len(row_word) == 9 and regex_matches_wordlist(row_word, valid_words):
        board[row][col] = 0  # Undo the placement
        return False

    # Check the column
    col_word = "".join(board[i][col] for i in range(9)).replace("0", "")
    if len(col_word) == 9 and regex_matches_wordlist(col_word, valid_words):
        board[row][col] = 0  # Undo the placement
        return False

    # Check the 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    box_letters = [
        board[i][j]
        for i in range(start_row, start_row + 3)
        for j in range(start_col, start_col + 3)
    ]
    box_word = "".join(box_letters).replace("0", "")
    if len(box_word) == 9 and regex_matches_wordlist(box_word, valid_words):
        board[row][col] = 0  # Undo the placement
        return False

    # Undo the temporary placement and return True
    board[row][col] = 0
    return True

def solve_sudoku(board):
    """Solve the Sudoku board using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_letter(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_solved_sudoku():
    valid_words = generate_nine_character_words()
    """Generate a solved Sudoku board."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            nums = list(string.ascii_lowercase[:9])
            random.shuffle(nums)
            for num in nums:
                if is_valid_letter(board, i, j, num, valid_words):
                    board[i][j] = num
                    break
    if not solve_sudoku(board):
        return generate_solved_sudoku()
    return board

def print_board(board):
    """Print the Sudoku board with grid lines."""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Horizontal line after every third row
        row_with_bars = [
            str(num) if (j + 1) % 3 != 0 else f"{num} |" for j, num in enumerate(row)
        ]
        print(" ".join(row_with_bars).rstrip("|"))  # Remove trailing bar

# Example usage
if __name__ == "__main__":
    try:
        import nltk
        nltk.download("words")
    except ImportError:
        print("Please install nltk using 'pip install nltk'.")

    solved_board = generate_solved_sudoku()
    print("Generated Solved Sudoku:")
    print_board(solved_board)
    print(len(generate_nine_character_words()))