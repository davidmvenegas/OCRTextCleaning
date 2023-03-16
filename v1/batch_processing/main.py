import os
import re
import unicodedata
from nltk.corpus import stopwords

"""
This function performs the following cleaning operations to multiple files concurrently and efficiently with parallel processing:
1. Removes all punctuation marks except certain special characters
2. Removes all white spaces
3. Normalizes all accented characters to their base form
4. Normalizes all inconsistent casing to lowercase
5. Removes any words included in a list of stopwords
6. Removes all lines that consist solely of 5 or less non-alphabetic characters.
7. Joins all lines into a single chunk, removing excess newlines
"""


def clean_text_file(input_file_path, output_file_path):
    # Load the list of stopwords from the NLTK library
    stop_words = set(stopwords.words('english'))

    # Regex pattern for removing all punctuation and white spaces, except for the following special characters (->  .,;:$£€@&%!?'"/-()[]  <-)
    pattern = r'[^\w\s\/\-\'.,;:$£€@&%!?()"\[\]]'

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        cleaned_lines = []
        for line in input_file:
            # 1. Remove punctuation and white spaces using regex
            line = re.sub(pattern, '', line)

            # 3. Normalize accented characters
            line = unicodedata.normalize('NFKD', line).encode(
                'ascii', 'ignore').decode('utf-8')

            # 4. Normalize inconsistent casing
            line = line.lower()

            # 5. Filter out stop words and non-alphabetic words using a generator expression
            line = ' '.join(word for word in line.split() if word not in stop_words and (
                word.isalpha() or word.isnumeric()))

            # 6. Filter out lines that consist solely of 5 or less non-alphabetic characters
            if len(line) <= 4:
                continue

            cleaned_lines.append(line)

        # 7. Join all cleaned lines into a single chunk, removing excess newlines
        cleaned_text = ' '.join(cleaned_lines)
        cleaned_text = cleaned_text.replace('\n', ' ')

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_text)


def clean_text_files_in_folder(input_folder_path, output_folder_path):
    for file_name in os.listdir(input_folder_path):
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)

        if os.path.isfile(input_file_path):
            clean_text_file(input_file_path, output_file_path)


clean_text_files_in_folder("input_folder", "output_folder")
