from my_shuffle.common import common
import random

def shuffle(x, y, w):
  def pos(song, weight, w_step):
    mode = 100.0 - (getattr(song, weight) - random.random())*w_step
    return random.triangular(0.0, 100.0, mode)
  
  w_max = max([getattr(x[i], w) for i in range(len(x))])
  w_step = 100.0 / w_max
  x.sort(key=lambda i: pos(i, w, w_step))
  common.shuffle(x, y, w)
