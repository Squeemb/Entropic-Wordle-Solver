import math
from collections import Counter

def getFeedback(guess, secret):
	"""
	Calculates the Wordle feedback pattern.
	0 = gray, 1 = yellow, 2 = green
	"""
	result = [0] * 5
	secretList = list(secret)
	guessList = list(guess)

	# Find greens in the correct positionz
	for i in range(5):
		if guessList[i] == secretList[i]:
			result[i] = 2
			secretList[i] = None  # Mark as used
			guessList[i] = None
	
	# Find yellows in the wrong position
	for i in range(5):
		if guessList[i] is not None and guessList[i] in secretList:
			result[i] = 1
			secretList[secretList.index(guessList[i])] = None
	return tuple(result)

def calculateEntropy(guess, possibleWords):
	"""
	Calculates the Shannon Entropy of a guess
	based on the remaining possible words.
	"""
	patterns = []
	for word in possibleWords:
		pattern = getFeedback(guess, word)
		patterns.append(pattern)

	# Count the frequency of each feedback pattern
	counts = Counter(patterns)
	totalWords = len(possibleWords)
	entropy = 0

	for count in counts.values():
		p = count / totalWords
		entropy -= p * math.log2(p)

	return entropy
