import re
from unidecode import unidecode

"""
Input/Output: TEXT

This function performs the following to clean the text:
1. Removes any lines containing more than a specified amount of punctuation.
2. Removes all punctuation marks except for the following special characters: .,;:$£€@&%!?'"/-()[].
3. Removes any excess white space, but don't join lines.
4. Normalizes all accented characters to their base form.
5. Capitalizes all words that are entirely uppercase.
6. Removes any entirely non-alphabetical lines.
7. Removes lines with 2 characters or less.
"""


def clean_text(raw_text):
    lines = raw_text.split("\n")
    cleaned_lines = []

    large_line = 16

    small_line_punctuation_threshold = 0.2
    large_line_punctuation_threshold = 0.4

    for line in lines:
        # Remove excess whitespace from line
        line = line.strip()

        # Calculate the total number of non-whitespace characters
        non_whitespace_chars = sum(
            1 for c in line if c not in set(" \t\n"))

        # Calculate the total number of punctuation characters
        punctuation_chars = sum(1 for c in line if c not in set(
            " \t\n") and c in set(".,;:$£€@&%!?'\"/-()[]"))

        # Calculate the punctuation ratio, or set it to a value that won't satisfy the condition if non_whitespace_chars is zero
        if non_whitespace_chars > 0:
            punctuation_ratio = punctuation_chars / non_whitespace_chars
        else:
            # Any value greater than punctuation_ would work
            punctuation_ratio = 1

        # Dynamically adjust the punctuation threshold based on non-whitespace character length
        if non_whitespace_chars > large_line:
            punctuation_threshold = large_line_punctuation_threshold
        else:
            punctuation_threshold = small_line_punctuation_threshold

        # Check if the line is not empty and the punctuation ratio is less than or equal to the dynamic punctuation threshold
        if line and punctuation_ratio <= punctuation_threshold:
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

    return "\n".join(cleaned_lines)


# Simulate passing raw text to the function
with open("input.txt", "r") as f:
    raw_text = f.read()

# Run the function
cleaned_text = clean_text(raw_text)

# Save the raw text to a file for comparison
with open("output.txt", "w") as f:
    f.write(cleaned_text)
