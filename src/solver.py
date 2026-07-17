import os
import requests
from datetime import date
from entropyCalc import calculateEntropy, getFeedback

def get_wordle_of_the_day():
    """
    Fetches today's Wordle answer from the NYT API.
    """

    today = date.today().strftime("%Y-%m-%d")
    url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data['solution'].upper()
    except Exception as e:
        print(f"Could not fetch today's word: {e}")
        return "CRANE" # If unable to fetch, return a default word

def load_dictionary(filename):
    """Stage 1: Load the wordlist from the data folder."""
    path = os.path.join("data", filename)
    with open(path, "r") as f:
        return [line.strip().upper() for line in f if len(line.strip()) == 5]

def solveWordle(secretWord, allWords):
    """
    Simulartes a Wordle game by maxxing out the entropy.
    """
    possibleWords = allWords.copy()
    attempts = 0

    print(f"Target word: {secretWord}")
    print(f"Initial uncertainty: {len(possibleWords)} possible words")

    while True:
        attempts += 1
        
        # 1) Finding the best guess; this is initally slow
        if attempts == 1:
            bestGuess = "TARES"  # Common high entropy starter
        else:
            # Rank all possible words by entropy with a greedy approach
            bestGuess = max(possibleWords, key=lambda word: calculateEntropy(word, possibleWords))
        
        # 2) Get feedback
        pattern = getFeedback(bestGuess, secretWord)

        print(f"Attempt {attempts}: Guesssing '{bestGuess}' -> Pattern: {pattern}")

        if bestGuess == secretWord:
            print(f"Solved in {attempts} turns.")
            return attempts

        # 3) Filter the dictionary
        # Keep the words that give the same pattern
        possibleWords = [
            w for w in possibleWords
            if getFeedback(bestGuess, w) == pattern
        ]

        print(f"Remaining words: {len(possibleWords)}")

if __name__ == "__main__":
    words = load_dictionary("wordlist.txt")
    
    # FETCH LIVE DATA
    target = get_wordle_of_the_day()
    print(f"Today's Real Wordle: {target}")
    
    solveWordle(target, words)
