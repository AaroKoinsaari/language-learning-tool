"""
Language Tool Program
Author: Aaro Koinsaari
Date: 2023-07-31
Version: 1.0.0

Description:
A simple console program for practicing French-English translations.
The program provides a quiz-like interface where users are prompted to translate words from one 
language to the other.
Currently quizzes are only from English to French and the user progress is not tracked.

Future Improvements:
- Addition of sentences
- Option to choose from English-to-French or French-to-English
- Tracking user progress
- Enhanced error handling and user input validation
- Enable user to add new words (or sentences) to the dictionary
- Addition of pronounciation audio as the word or sentence is presented
- Support for some other languages
- Addition of a GUI
"""


import csv
import random
import os


def load_dictionary(file_path):
    """
    Loads a dictionary of English-xx word pairs from a csv-file.

    Args:
        file_path (str): The path to the csv-file.

    Returns:
        list: A list of tuples containing English and the other language word pairs.
    """

    # File not found
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    
    dictionary = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader) # Skip the header
    
            # Go through and add each word and its translation to the dictionary list
            for row in reader:
                dictionary.append((row[0], row[1]))
                
    except Exception as e:
        print(f"An error has occurred while reading the file: {e}")
        exit(1)
    
    return dictionary


def main():
    """
    Loads the dictionary file, shuffles its content, and
    prompts the user to translate the words. Exit is handled
    by typing 'q'.
    """    

    print("""
    Welcome to the Simple Language Learning Game!
    ------------------------------------------
    This console program will test your knowledge of word translations.
    You'll be given English words, and your task is to translate them into French.

    To start a new word challenge, just press Enter.
    If you want to exit the program at any time, write 'q' and press Enter.

    Bonne chance!

    """)
    
    dictionary = load_dictionary("../data/dictionary_french.csv")
    random.shuffle(dictionary)

    for english, french in dictionary:
        attempts = 2 # Adjust the attempts for right answer
        
        while attempts > 0:
            user_input = input(f"Write in French: {english}\n")
            if user_input.lower().strip() == 'q':
                print("Exiting the game!")
                return
            elif user_input.lower().strip() == french.lower():
                print("Correct!\n")
                break
            else:
                attempts -= 1 # Wrong answer
                if attempts > 0:
                    print("Wrong! You have {attempts} attempts left.\n")
                else: # No attempts left
                    print(f"Wrong! The correct translation is {french}\n")

    print("Game over!")

if __name__ == '__main__':
    main()
