from collections import Counter
from collections import defaultdict
import random
from multiprocessing import Pool

def genResString(stnums, symbols):
    output = ''
    for (num, symb) in zip(stnums, symbols):
      output += num + symb
    output += stnums[-1]
    return output

def add_zeros(sts, symbols):
  count = sum(len(s) for s in sts) + len(symbols)
  if count >= 6:
    return [genResString(sts, symbols)]
  elif count >= 5:
    out = []
    for i in range(len(sts)):
      temp = [st for st in sts]
      temp[i] = '0' + temp[i]
      out.append(genResString(temp, symbols))
    return out
  else:
    output = []
    for i in range(len(sts)):
      temp = [st for st in sts]
      temp[i] = '0' + temp[i]
      output += add_zeros(temp, symbols)
    return output

def onesymbhelper(symbol):
  out = []
  for num1 in range(0, 10**5):
    for num2 in range(0, 10**5):
      if symbol == '/' and num2 == 0:
        continue
      st1 = str(num1)
      st2 = str(num2)
      res = eval(st1 + symbol + st2)
      if symbol == '/' and res != int(res):
        continue
      stres = str(int(res))
      if len(st1) + len(st2) + len(stres) + 2 > 6:
        break
      out += add_zeros([st1, st2, stres], [symbol, '='])
  return out

if __name__ == '__main__':
  word_length = 6
  guesses = 6

  # raw_words = list(filter(lambda w: len(w) == word_length, map(lambda w: w.strip(), open('words.txt').readlines())))
  # common_words = map(lambda word: word.strip(), open('common_words.txt').readlines())
  letters = '0123456789+-*/'

  # only equals
  onlyeq = []

  for num in range(0, 100):
    n = str(num)
    onlyeq += add_zeros([n, n], ['='])

  print(onlyeq[0], onlyeq[-1], len(onlyeq))

  onesymbol = []

  # one plus symbol.

  temp = []
  with Pool(4) as p:
    temp = p.map(onesymbhelper, '+-*/')

  for t in temp:
    onesymbol += t

  onesymbol = list(set(onesymbol))
  print(onesymbol[0], onesymbol[-1], len(onesymbol))

  raw_words = onlyeq + onesymbol

  with open('miniwords.txt', 'w') as f:
    f.write('\n'.join(set(raw_words)))