"""
Simple Language Learning Tool
Author: Aaro Koinsaari
Date: 2023-08-02
Version: 1.1.0

Description:
A simple console program for practicing French-English translations.
The program provides a quiz-like interface where users are prompted to translate words from one 
language to the other.
Currently, the user progress is not tracked.

Future Improvements:
- Addition of sentences
- Tracking user progress
- Enhanced error handling and user input validation
- Enable user to add new words (or sentences) to the dictionary
- Addition of pronunciation audio as the word or sentence is presented
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
            next(reader)  # Skip the header

            # Go through and add each word and its translation to the dictionary list
            for row in reader:
                dictionary.append((row[0], row[1]))

    except Exception as e:
        print(f"An error has occurred while reading the file: {e}")
        exit(1)

    return dictionary


def select_translation_direction():
    """
    Prompts the user to choose the direction of translation.

    Returns:
        str: '1' for English to French and '2' for French to English.
    """

    print("""
    Choose the translation direction:
    1: English to French
    2: French to English
    """)

    choice = input("Enter 1 or 2:").strip()

    while choice not in ['1', '2']:
        print("Invalid choice!")
        choice = input("Enter 1 or 2:").strip()

    return choice


def play_game(dictionary, choice):
    """
    Plays the translation game based on the provided dictionary and user's choice of translation direction.

    Args:
        dictionary (list): A list of tuples containing word pairs in English and the target language.
        choice (str): A string representing the user's choice of translation direction.
                     '1' for English to target language,
                     '2' for target language to English.

    Returns:
        None: The function prints the game process to the console and returns None. If the user chooses to exit,
              the function prints an exit message and returns.
    """

    # Iterate through the dictionary until exit signal is given
    for english, french in dictionary:
        if choice == '1':
            prompt, answer = english, french  # English to French
        else:
            prompt, answer = french, english  # French to English

        attempts = 3  # Adjust the attempts for right answer

        # Keep the game going in a loop until the quit signal is given
        while attempts > 0:
            user_input = input(f"Write the translation: {prompt}\n")
            if user_input.lower().strip() == 'q':
                print("Exiting the game!")
                return
            elif user_input.lower().strip() == answer.lower():
                print("Correct!\n")
                break
            else:
                attempts -= 1  # Wrong answer
                if attempts > 0:
                    print(f"Wrong! You have {attempts} attempts left.\n")
                else:  # No attempts left
                    print(f"Wrong! The correct translation is {answer}\n")


def main():
    """
        Initializes the Simple Language Learning Tool:
        - Prints a welcome message and the instructions for the game.
        - Prompts the user to select the translation direction (English to French or vice versa).
        - Loads the dictionary file containing word pairs.
        - Shuffles the dictionary.
        - Calls the play_game function to start the game, passing in the dictionary and user's choice.
        - Exit is handled by typing 'q' within the play_game function.

    Returns:
        None
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

    choice = select_translation_direction()

    dictionary = load_dictionary("../data/dictionary_french.csv")
    random.shuffle(dictionary)

    play_game(dictionary, choice)


if __name__ == '__main__':
    main()
