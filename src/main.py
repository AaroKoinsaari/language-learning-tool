"""
Simple Language Learning Tool
Author: Aaro Koinsaari
Date: 2023-08-02
Version: 1.1.0

Description:
A simple console program for practicing French-English translations.
The program provides a quiz-like interface where users are prompted to translate words from one 
language to the other while tracking user progress by keeping track of failed attempts for each
word.

Future Improvements:
- Addition of sentences
- Enhanced tracking of user progress
- Enhanced error handling and user input validation
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

    dictionary = []  # Initialize dictionary for word-translation pairs
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


def get_prompt_answer(choice, source, target):
    """
    Determines the prompt and answer based on the user's choice of translation direction.

    Args:
        choice (str): A string representing the user's choice of translation direction.
                      '1' for source to target language,
                      '2' for target language to source.
        source (str): The word in the source language.
        target (str): The word in the target language.

    Returns:
        tuple: A tuple containing the prompt and answer for the translation.
    """

    if choice == '1':
        return source, target
    else:
        return target, source


def save_word(username, user_input, word):
    """
    Saves a user-specified word and its corresponding translation into a CSV file.
    The file is specific to the given username, allowing individualized tracking of saved words.
    This function is typically called when the user wants to add a word to their personal dictionary.

    Args:
        username (str): The username of the player. Used to determine the specific file for saving the word.
        user_input (str): The word as inputted by the user.
        word (str): The translation or corresponding value of the user's inputted word.

    Returns:
        None: The function writes to the file and does not return a value.
    """

    with open(f"../data/{username}_dictionary.csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([user_input, word])


def add_incorrect_word(word, username):
    """
    Adds or updates an incorrect word in the user's progress file, identified by the username.
    If the word already exists in the file, the function increments its incorrect attempt count by 1.
    If the word does not exist, it adds a new entry for the word with an incorrect attempt count of 1.

    Args:
        word (str): The word that the user got incorrect.
        username (str): The username of the player. Used to determine the specific file for tracking progress.

    Returns:
        None
    """

    incorrect_words = {}  # Create dictionary to hold the incorrect word-attempt pairs
    try:
        # Open the user progress file in reading-mode
        with open(f"../data/{username}_progress.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Skip the header row

            # Iterate through the rows, adding each word and its attempts to the dictionary
            # TODO: Issue if two or more incorrect answers for the same word. Throws IndexError
            for row in reader:
                incorrect_words[row[0]] = int(row[1])

    except FileNotFoundError:  # Create the file later if it doesn't exist
        pass

    # Increment the count for the given word or set it to 1 if the word is not in the dictionary
    incorrect_words[word] = incorrect_words.get(word, 0) + 1

    # Open the file in writing-mode
    with open(f"../data/{username}_progress.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['word', 'incorrect_attempts'])  # Header row

        # Iterate over the incorrect_words dictionary and write a row for each word and
        # its corresponding incorrect attempt count
        for word, attempts in incorrect_words.items():
            writer.writerow([word, attempts])


def create_user_file(username):
    """
    Retrieves the user's progress file if it exists or creates a new one if it doesn't.
    The progress file is specific to the given username and tracks incorrect attempts at word translations.

    Args:
        username (str): The username of the player. Used to determine the specific file for tracking progress.

    Returns:
        str: The file path to the user's progress file. This file will either be newly created or already exist.
    """

    file_path = f"../data/{username}_progress.csv"

    if not os.path.exists(file_path):  # Create a new progress file
        print(f"Welcome, {username}! Creating a new user profile for you.")
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['word', 'incorrect_attempts'])  # Header row
    else:  # Username and its progress file exists
        print(f"Welcome back, {username}!")


def play_game(username, dictionary, choice):
    """
    Plays the translation game based on the provided dictionary and user's choice of translation direction.
    Keeps track of incorrect attempts and allows the user to save words to their dictionary.

    Args:
        username (str): Player's username.
        dictionary (list): A list of tuples containing word pairs in English and the target language.
        choice (str): A string representing the user's choice of translation direction.
                      '1' for English to target language,
                      '2' for target language to English.

    Returns:
        None: The function prints the game process to the console and returns None. If the user chooses to exit,
              the function prints an exit message and returns.
    """

    # Iterate through the dictionary until the exit signal is given
    for english, french in dictionary:
        prompt, answer = get_prompt_answer(choice, english, french)  # Determine the translation direction

        attempts = 3  # Adjust the attempts for right answer

        # Keep the game going in a loop until the quit signal is given
        while attempts > 0:
            user_input = input(f"Write the translation: {prompt}\n")

            # Quit signal
            if user_input.lower().strip() == 'q':
                print("Exiting the game!")
                return

            # Save word in own dictionary
            elif user_input.lower().strip() == 's':
                save_word(username, user_input.lower().strip(), answer)
                print("Word and its translation saved in dictionary!\n")

            # Correct answer
            elif user_input.lower().strip() == answer.lower():
                print("Correct!\n")
                break

            # Wrong answer
            else:
                attempts -= 1
                add_incorrect_word(answer, username)  # Collect failed words to monitor user progress
                if attempts > 0:
                    print(f"Wrong! You have {attempts} attempts left.\n")
                else:  # No attempts left
                    print(f"Wrong! The correct translation is {answer}\n")


def main():
    """
    Initializes the Simple Language Learning Tool:
    - Prints a welcome message and the instructions for the game.
    - Prompts the user for a username.
    - Manages user's progress file based on the username.
    - Prompts the user to select the translation direction (English to target language or vice versa).
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

    # Handle the user progress by the username
    user = input("Please, enter your username: ")
    create_user_file(user)

    choice = select_translation_direction()

    dictionary = load_dictionary("../data/dictionary_french.csv")
    random.shuffle(dictionary)

    play_game(user, dictionary, choice)


if __name__ == '__main__':
    main()
