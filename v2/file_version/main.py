import re
from unidecode import unidecode

"""
Input/Output: FILES

This function performs the following to clean the text:
1. Removes any lines consisting of over 20% of punctuation, not counting whitespace.
2. Removes all punctuation marks except for the following special characters: .,;:$£€@&%!?'"/-()[].
3. Removes any excess white space, but don't join lines.
4. Normalizes all accented characters to their base form.
5. Capitalizes all words that are entirely uppercase.
6. Removes any entirely non-alphabetical lines.
7. Removes lines with 2 characters or less.
"""


def clean_text(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    cleaned_lines = []
    punctuation_threshold = 0.2

    for line in lines:
        # Remove excess whitespace from line
        line = line.strip()

        # Calculate proportion of non-whitespace characters that are punctuation
        if line.strip() and sum(1 for c in line if c not in set(" \t\n") and c in set(".,;:$£€@&%!?'\"/-()[]")) / sum(1 for c in line if c not in set(" \t\n")) <= punctuation_threshold:
            # Remove unwanted punctuation
            line = re.sub(r"[^\w\s.,;:$£€@&%!?'\"/\-\(\)\[\]]", "", line)

            # Normalize accented characters
            line = unidecode(line)

            # Capitalize uppercase words
            words = []
            for word in line.split():
                if word.isupper():
                    words.append(word.capitalize())
                else:
                    words.append(word)
            line = " ".join(words)

            # Remove lines that are entirely non-alphabetical or less than three characters
            if any(c.isalpha() for c in line) and len(line) >= 3:
                cleaned_lines.append(line)

    with open(output_file, "w") as f:
        f.write("\n".join(cleaned_lines))


clean_text("input.txt", "output.txt")
