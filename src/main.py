"""
Simple Language Learning Tool
Author: Aaro Koinsaari
Date: 2023-09-30
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

"""
TODO fixes:
    - Ask same word multiple times
    - Make answer checking case insensitive and trim possible whitespace and "..."
    - Make user choose translation direction
    - Implement user progress:
        - user's own dictionary to save and delete words
        - user progress tracking to enhance learning
    - Quit signal implementation
"""


class Dictionary:
    """This class serves as a representation of a language dictionary.

    Attributes:
        word_dict (dict): A dictionary to store words along with their phrases and translations.
    """

    def __init__(self, initial_data=None):
        """Initializes the Dictionary with given data or as empty."""
        self.word_dict = initial_data if initial_data else {}

    def add_word(self, main_word, phrases, translations):
        """Adds a new word along with its phrases and translations to the dictionary."""
        self.word_dict[main_word] = {
            "phrases": phrases,
            "translations": translations
        }

    def remove_word(self, user_word):
        """Removes a word from the dictionary."""
        main_word = self.find_main_word(user_word)
        if main_word:
            del self.word_dict[main_word]
            return True  # Successfully removed
        else:
            return False  # TODO: handling for not finding the word

    def check_translation(self, user_word, user_translation):
        """Checks if the user's translation is correct."""
        main_word = self.find_main_word(user_word)
        if main_word:
            correct_translations = [t.lower() for t in self.word_dict[main_word]['translations']]
            return user_translation.lower() in correct_translations
        return False

    def find_main_word(self, user_word):
        """Finds the main word associated with the word provided by the user."""
        for main_word, details in self.word_dict.items():
            if user_word.lower() in [phrase.lower() for phrase in details['phrases']]:
                return main_word
        return None

    def get_random_word(self):
        """Returns a random word for the quiz."""
        # TODO: Implement this method
        pass


class Quiz:
    """This class handles the quiz logic.

    Attributes:
        dictionary (Dictionary): An instance of the Dictionary class.
        score (int): The current score of the quiz.
    """
    def __init__(self, dictionary_instance):
        """Initializes the Quiz with a given Dictionary instance."""
        self.dictionary = dictionary_instance
        self.score = 0

    def ask_question(self):
        """Asks a random question based on the words in the dictionary and validates the user's answer."""
        main_word, details = random.choice(list(self.dictionary.word_dict.items()))

        # Ask the user for the translation and validate
        user_translation = input(f"What is the translation of {main_word}? ")
        is_correct = self.dictionary.check_translation(main_word, user_translation)

        # Update score and provide feedback
        if is_correct:
            self.score += 1
            print("Correct!")
        else:
            print("Incorrect.")

    def start_game(self):
        """Starts the game loop and asks a fixed number of questions for now."""
        for _ in range(5):
            self.ask_question()

        print(f"Your final score is: {self.score}")


class FileHandler:
    """This class handles file read and write operations.

    Attributes:
        file_path (str): The path to the file to be read/written.
    """
    def __init__(self, file_path):
        # The path to the file to be read/written
        self.file_path = file_path

    def read_from_file(self):
        """Reads data from the file and returns it as a dictionary."""
        data_dict = {}
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                joined_row = ",".join(row)
                phrases, translations = joined_row.split(";")

                # Split phrases and translations by commas
                phrase_list = phrases.split(",")
                translation_list = translations.split(",")

                # Store in the dictionary
                main_phrase = phrase_list[0]  # First phrase as key
                data_dict[main_phrase] = {
                    "phrases": phrase_list,
                    "translations": translation_list
                }
        return data_dict

    def write_to_file(self, data):
        """Writes the given data to the file."""
        with open(self.file_path, 'w') as file:
            writer = csv.writer(file)
            for main_phrase, details in data.items():
                phrases = ",".join(details["phrases"])
                translations = ",".join(details["translations"])
                writer.writerow([f"{phrases};{translations}"])


class LanguageTool:
    """This class serves as the main controller for the Language Learning Tool.

    Attributes:
        file_handler (FileHandler): An instance of the FileHandler class to handle file operations.
        dictionary (Dictionary): An instance of the Dictionary class to manage words and translations.
        quiz (Quiz): An instance of the Quiz class to handle the quiz logic.
    """
    def __init__(self):
        """Initializes the LanguageTool with None values for its attributes."""
        self.file_handler = None
        self.dictionary = None
        self.quiz = None

    def initialize_app(self):
        """Initializes the main components and starts the quiz."""
        self.file_handler = FileHandler("../data/dictionary_french.csv")
        initial_data = self.file_handler.read_from_file()
        self.dictionary = Dictionary(initial_data)
        self.quiz = Quiz(self.dictionary)
        self.quiz.start_game()


if __name__ == "__main__":
    app = LanguageTool()
    app.initialize_app()
