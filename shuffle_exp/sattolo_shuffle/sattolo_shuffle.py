import random
 
def shuffle(x):
  for i in range(len(x)-1, 0, -1):
    j = random.randrange(i)
    x[i], x[j] = x[j], x[i]
