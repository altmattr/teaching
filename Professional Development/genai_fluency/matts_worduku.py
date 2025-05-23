from time import sleep
from nltk.corpus import words
import re
import random
import string

size = 6
box_on = True
solutions = []

def regex_matches_wordlist(regex, word_list, label="Some"):
    pattern = re.compile(regex)  # Compile the regex for efficiency
    for word in word_list:
        if pattern.fullmatch(word.lower()):  # Check for a full match
            return True
    return False

def try_letter_at(letter, index, board):
    if index > size * size - 1:
        return True
    row =index // size
    col = index % size
    if index >= 0:
        board[row][col] = letter
    print(f"\033[HTrying {letter} at ({row}, {col})")
    for r in range(size):
        print(" ".join(board[r]))
    # sleep(0.05)
    # check is this is valid
    valid = True
    if(index >= 0):
        row_word = "".join(board[row])
        valid = valid and regex_matches_wordlist(row_word, valid_words,"row")
        col_word = "".join(board[i][col] for i in range(size))
        valid = valid and regex_matches_wordlist(col_word, valid_words, "col")
        # # check the 3x3 box
        # start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        # box_letters = [
        #     board[i][j]
        #     for i in range(start_row, start_row + 3)
        #     for j in range(start_col, start_col + 3)
        # ]
        # box_word = "".join(box_letters)
        # valid = valid and regex_matches_wordlist(box_word, valid_words, "box")
    if valid:
        print("valid - next letter")
        for l in list(string.ascii_lowercase):
            result = try_letter_at(l, index + 1, board)
            if result:
                break 
        return result
    else:
        print("invalid - backtrack")
        board[row][col] = "."
        return False


if __name__ == "__main__":
    import nltk
    nltk.download("words")

    board = [["." for _ in range(size)] for _ in range(size)]
    word_list = words.words()
    valid_words = [
        word for word in word_list if len(word) == size and len(set(word)) == size
    ]
    print("\033[2J")
    try_letter_at("a", -1, board)
    print("done")
    # print the board
    for r in range(size):
        print(" ".join(board[r]))
