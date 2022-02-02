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
  if count >= 8:
    return [genResString(sts, symbols)]
  elif count >= 7:
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
      if len(st1) + len(st2) + len(stres) + 2 > 8:
        break
      out += add_zeros([st1, st2, stres], [symbol, '='])
  return out

def twosymbhelper(symbols):
  out = []
  (s1, s2) = symbols
  for n1 in range(100):
    for n2 in range(100):
      if s1 == '/' and n2 == 0:
        continue
      for n3 in range(100):
        if s2 == '/' and n3 == 0:
          continue
        st1 = str(n1)
        st2 = str(n2)
        st3 = str(n3)
        res = eval(st1 + s1 + st2 + s2 + st3)
        if res != int(res):
          continue
        stres = str(int(res))
        if len(st1) + len(st2) + len(st3) + len(stres) + 3 <=8:
          out += add_zeros([st1, st2, st3, stres], [s1, s2, '='])
  return out

if __name__ == '__main__':
  word_length = 8
  guesses = 6

  # raw_words = list(filter(lambda w: len(w) == word_length, map(lambda w: w.strip(), open('words.txt').readlines())))
  # common_words = map(lambda word: word.strip(), open('common_words.txt').readlines())
  letters = '0123456789+-*/'

  # only equals
  onlyeq = []

  for num in range(0, 1000):
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

  twosymbs = []
  temp = []
  with Pool(4) as p:
    temp = p.map(twosymbhelper, [(i1, i2) for i1 in '+-*/' for i2 in '+-*/'])
  
  for t in temp:
    twosymbs += t

  print(twosymbs[0], twosymbs[-1], len(twosymbs))

  raw_words = onlyeq + onesymbol + twosymbs

  with open('words.txt', 'w') as f:
    f.write('\n'.join(set(raw_words)))