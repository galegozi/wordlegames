from collections import Counter
from collections import defaultdict
import random

word_length = 8
guesses = 6

raw_words = list(filter(lambda w: len(w) == word_length, map(lambda w: w.strip(), open('words.txt').readlines())))
letters = '0123456789+-*/'

def removeIfPresent(st, elem):
  if elem in st:
    st.remove(elem)
  return st

class CharInfo:
  def __init__(self):
    self.correctChar = ''
    self.wrongPos = set()

class WordInfo:
  def __init__(self, length, raw_words, guesses):
    self.invalidChars = set()
    self.unknown = set(letters)
    self.charList = list(map(lambda _: CharInfo(), range(length)))
    self.raw_words = raw_words
    self.options = [word for word in raw_words]
    self.frequency = self.getFrequencyDict()
    self.avail_guesses = guesses
    self.aggressive = True
    self.optionsFrequencies = self.getFrequencyDict()
  def getFrequencyDict(self):
    return Counter(''.join(self.options))
  def aggressiveGuess(self):
    self.optionsFrequencies = self.getFrequencyDict()
    def keyFxn(word):
      unknown = -1*len([ch for ch in set(word) if ch in self.unknown])
      wrongPos = -1*sum(len([w for w in set(word) if w in ch.wrongPos]) for ch in self.charList)
      freq = -1*sum(self.optionsFrequencies[w] for w in set(word))
      return (unknown, wrongPos, freq)
    return list(sorted(self.raw_words, key = keyFxn))[0]
  def nonAgressiveGuess(self):
    def sortHelp(words):
      return list(sorted(words, key = lambda word: sum(map(lambda l: self.frequency[l], set(word))), reverse=True))
    singles = sortHelp([word for word in self.options if len(set(word)) == len(word)])
    combined = singles + sortHelp(self.options)
    return combined[0]
  def parseGuess(self, pred, info):
    if 'X' not in guess and 'V' not in guess:
      self.aggressive = False
    for (i, (g, m)) in enumerate(zip(pred, info)):
      if len(self.options) <= 1:
        print('breaking!', self.options)
        break
      if m == 'X':
        num = current.count(g)
        self.options = list(filter(lambda word: word.count(g) < num, self.options))
        self.charList[i].wrongPos.add(g)
        removeIfPresent(self.unknown, g)
      elif m == 'V':
        self.invalidChars.add(g)
        self.options = list(filter(lambda word: g not in word, self.options))
        removeIfPresent(self.unknown, g)
      elif m == 'G':
        self.charList[i].correctChar = g
        self.options = list(filter(lambda word: word[i] == g, self.options))
        removeIfPresent(self.unknown, g)
      elif m == 'Y':
        self.charList[i].wrongPos.add(g)
        self.options = list(filter(lambda word: word[i]!= g and g in word, self.options))
        removeIfPresent(self.unknown, g)
  def make_guess(self):
    if self.avail_guesses <= 1 or len(self.options) <= 1 or len(self.options) <= self.avail_guesses:
      self.aggressive = False
      print('DISABLING AGGRESSIVE GUESSING')
    self.avail_guesses -= 1
    if self.aggressive:
      return self.aggressiveGuess()
    else:
      return self.nonAgressiveGuess()

myword = WordInfo(word_length, raw_words, guesses)

# chosen = random.choice(raw_words)
# print('chosen =', chosen)

current = myword.make_guess()

def checkGuess(pred, actual):
  print('GUESSING', pred, 'FOR WORD', actual)
  def predChar(obj):
    (p, a) = obj
    if p == a:
      return 'G'
    elif p in actual:
      if actual.count(p) < pred.count(p):
        return 'X'
      else:
        return 'Y'
    else:
      return 'V'
  return ''.join(map(predChar, zip(pred, actual)))

for _ in range(guesses):
  print('Guess: ', current)
  print(len(myword.options))
  guess = input("What did it say? ")
  # guess = checkGuess(current, chosen)
  print('CHECK GUESS GIVES', guess)
  if guess == "" or guess == "G" * word_length:
    break
  myword.parseGuess(current, guess)
  current = myword.make_guess()

# if guess == "" or guess == "G" * word_length or current == chosen:
#     print('The correct word is:', chosen)
# else:
#   print('incorrect!', current, chosen, checkGuess(current, chosen))
