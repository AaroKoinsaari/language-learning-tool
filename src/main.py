"""
Simple Language Learning Tool
Author: Aaro Koinsaari
Date: 2023-08-12
Version: 1.3.0

Description:
A console-based program for practicing French-English translations with support for both single words and sentences.
The program offers a quiz-like interface, prompting users to translate from one language to the other.
It tracks user progress by recording failed attempts for each word or sentence. No usage for tracking yet.
Users can add words or sentences to their personal dictionary for further practice. No usage for that yet.

Future Improvements:
- Usage for personal dictionary.
- Enhanced tracking of user progress with analysis.
- Enhanced error handling and user input validation.
- Introduction of pronunciation audio as the word or sentence is presented.
- Expansion to support additional languages.
- Development of a Graphical User Interface (GUI).
"""

import csv
import random
import os


def load_dictionary(file_path):
    """
    Loads a dictionary of English-xx word pairs from a CSV file, accommodating multiple translations.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of tuples. Each tuple contains:
            - A list of English phrases/sentences.
            - A list of their corresponding translations in the target language.
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

            # Go through and add each word/sentence and its translations to the dictionary list
            for row in reader:
                english_items = row[0].split(',')
                translations = row[1].split(',')
                dictionary.append((english_items, translations))

    except Exception as e:
        print(f"An error has occurred while reading the file: {e}")
        exit(1)

    return dictionary


# TODO: Delete this and implement it to main function.
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


# TODO: Fix the double quote when saving pairs that have multiple correct answers
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


def create_user_files(username):
    """
    Retrieves the user's progress file if it exists or creates a new one if it doesn't.
    The progress file is specific to the given username and tracks incorrect attempts at word translations.

    Args:
        username (str): The username of the player. Used to determine the specific file for tracking progress.

    Returns:
        str: The file path to the user's progress file. This file will either be newly created or already exist.
    """

    progress_file_path = f"../data/{username}_progress.csv"
    dictionary_file_path = f"../data/{username}_dictionary.csv"

    # Create the progress file
    if not os.path.exists(progress_file_path):
        print(f"Welcome, {username}! Creating a new user profile for you.")
        with open(progress_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['word', 'incorrect_attempts'])  # Header row
        with open(dictionary_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['word', 'translation'])  # Header row
    else:  # Username with its progress file and personal dictionary file exists
        print(f"Welcome back, {username}!")


def play_game(username, dictionary, choice):
    """
    Plays the translation game based on the provided dictionary and user's choice of translation direction.
    The game supports multiple correct translations for both single words and sentences.
    It also tracks incorrect attempts and allows the user to save words or sentences to their personal dictionary.

    Args:
        username (str): Player's username.
        dictionary (list): A list of tuples. Each tuple contains:
            - A list of English phrases/sentences.
            - A list of their corresponding translations in the target language.
        choice (str): A string representing the user's choice of translation direction.
                      '1' for English to target language,
                      '2' for target language to English.

    Returns:
        None: The function prints the game process to the console and returns None. If the user chooses to exit,
              the function prints an exit message and returns.
    """

    def get_prompt_answer(translation_direction, english_phrases, target_translations):
        """
        Determines the translation prompt and the set of correct answers based on the user's choice of
        translation direction and the available translations in the dictionary.

        Args:
            translation_direction (str): User's choice of translation direction.
            english_phrases (list): List of English phrases/sentences.
            target_translations (list): List of translations in the target language.

        Returns:
            tuple: A tuple containing the translation prompt and a list of correct answers.
        """

        if translation_direction == '1':  # English to French
            translation_prompt = random.choice(english_phrases)
            correct_answers = target_translations
        else:  # French to English
            translation_prompt = random.choice(target_translations)
            correct_answers = english_phrases
        return translation_prompt, correct_answers

    # Iterate through the dictionary until the exit signal is given
    for english_items, translations in dictionary:
        prompt, answers = get_prompt_answer(choice, english_items,
                                            translations)  # Determine the translation direction

        attempts = 3  # Adjust the attempts for right answer

        # Keep the game going in a loop until the quit signal is given
        while attempts > 0:
            print(f"Translate: {prompt}")
            user_input = input("Your translation: ").rstrip("...").strip()  # Remove "..." and trim spaces

            # Quit signal
            if user_input.lower().strip() == 'q':
                print("Exiting the game!")
                return

            # Save the prompted word in the personal dictionary
            elif user_input.lower().strip() == 's':
                save_word(username, prompt, ', '.join(answers))  # Save all possible answers
                print("Word and its translation saved in dictionary!\n")
                continue

            # User wants to add a new word to the personal dictionary
            elif user_input.lower().strip() == 'add word':
                english_word = input("Enter the English word: ")
                french_word = input("Enter the French word: ")
                save_word(username, english_word, french_word)
                print("Word added to your personal dictionary!\n")
                continue

            # TODO: Add sentences to personal dictionary with multiple values
            # # User wants to add a new sentence to the personal dictionary
            # elif user_input.lower().strip() == 'add word':
            # english_sentence = input("Enter the English sentence: ")
            # french_sentence = input("Enter the French sentence: ")
            # save_word(username, english_sentence, french_sentence)
            # print("Sentence added to your personal dictionary!\n")
            # continue

            else:
                # Normalize the user's input by converting to lowercase, removing trailing ellipses, and trimming spaces
                normalized_user_input = user_input.lower().rstrip("...").strip()

                # Normalize all the correct answers
                normalized_answers = [ans.lower().rstrip("...").strip() for ans in answers]

                # Check the normalized versions to determine if the answer is correct
                if normalized_user_input in normalized_answers:
                    print("Correct!\n")
                    break

                # Wrong answer
                else:
                    attempts -= 1
                    add_incorrect_word(prompt, username)  # Collect failed words to monitor user progress
                    if attempts > 0:
                        print(f"Wrong! You have {attempts} attempts left.\n")
                    else:  # No attempts left
                        print(f"Wrong! The correct translations are: {', '.join(answers)}\n")


def main():
    """
    Initializes the Simple Language Learning Tool:
    - Prints a welcome message and the instructions for the game.
    - Prompts the user for a username.
    - Manages user's progress file based on the username.
    - Prompts the user to select the translation direction (English to target language or vice versa).
    - Loads the dictionary file containing word/sentence pairs.
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
    create_user_files(user)

    choice = select_translation_direction()

    dictionary = load_dictionary("../data/dictionary_french.csv")
    random.shuffle(dictionary)

    play_game(user, dictionary, choice)


if __name__ == '__main__':
    main()
