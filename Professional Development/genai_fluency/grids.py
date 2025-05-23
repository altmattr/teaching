import itertools
from nltk.corpus import words

def generate_valid_grids(x, y, valid_words):
    valid_grids = []
    valid_words_set = set(valid_words)  # Use a set for faster lookups

    # Generate all possible combinations of rows
    for rows in itertools.product(valid_words, repeat=x):
        # Check if all columns form valid words
        columns = ["".join(row[col] for row in rows) for col in range(y)]
        if all(col in valid_words_set for col in columns):
            valid_grids.append(rows)

    return valid_grids

# Example usage
if __name__ == "__main__":
    import nltk
    nltk.download("words")
    valid_words = words.words()
    
    x, y = 3, 3  # Grid dimensions
    grids = generate_valid_grids(x, y, valid_words)

    print(f"Found {len(grids)} valid grids:")
    for grid in grids:
        for row in grid:
            print(row)
        print()