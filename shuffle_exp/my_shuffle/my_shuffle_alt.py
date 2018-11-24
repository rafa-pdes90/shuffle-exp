from my_shuffle.common import common
import random

def shuffle(x, y, w):
  x.sort(key=lambda i: -random.random() ** (1.0 / getattr(i, w)))
  common.shuffle(x, y, w)
